# coding=utf-8

import threading
import os
import os.path
import uuid
import requires


class CutVideo(threading.Thread):
    """
    Allow extract frames from video:
        To avoid unexpected result or send uncompleted images I will store file names at queue to consume them until
        complete sent every file
    """

    COMMAND = (
        "ffmpeg -i %s -vf " +
        "\"select=between(t\,%s\,60),scale=640:480,drawbox=x=0:y=0:w=400:h=30:color=black@1.0:t=max," +
        "drawtext=x=5:fontfile=/usr/share/fonts/gnu-free/FreeSans.ttf:y=5:fontcolor=white:text='%s" +
        "{pts\:localtime\:%s}'\" -r 1 -f image2 -qscale:v 5 %s"
    )

    PROVISIONAL_COMMAND = (
        "ffmpeg -i %s -ss 00:00:%s.0 -vframes 1 %s"
    )

    queue = []
    sufix = None

    def __init__(self, path_to_video, db):
        """

        :param path_to_video:
        :param database.DBConnection db:
        """
        super(CutVideo, self).__init__()
        self.path_to_video = path_to_video
        self.db = db
        self.sufix = uuid.uuid4()

        requires.logger.debug("CutVideo instance to '%s' path video" % self.path_to_video)

    def run(self):
        self.extract_frames()

    def extract_frames(self):
        """

        :return:
        """
        image_name = None

        # Sixty seconds to extract two frames by each one
        for i in range(0, 60):
            image_name = (
                requires.config.get("runtime", "path") +
                "/" +
                "img%s_%s_%s.jpeg" % (requires.config.get("runtime", "ticket"), i, str(self.sufix))
            )
            self.queue.append(image_name)

            command = self.PROVISIONAL_COMMAND % (
                self.path_to_video,
                i,
                image_name
            )
            requires.logger.debug("Extract image: %s" % image_name)

            os.system(command)

        self.start_send_images()

    def start_send_images(self):
        """

        :return:
        """
        while True:
            if 0 == len(self.queue):
                break

            i_image = self.queue[0]
            if os.path.isfile(i_image):
                requires.logger.debug("Sending image: '%s'" % i_image)
                # Sending
                del self.queue[0]
