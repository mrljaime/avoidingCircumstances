import threading
import time
import requires


class CutVideo(threading.Thread):

    COMMAND = (
    "ffmpeg -i %s/tmp/vid-%06d-2.avi -vf " +
    "\"select=between(t\,%s\,60),scale=640:480,drawbox=x=0:y=0:w=400:h=30:color=black@1.0:t=max," +
    "drawtext=x=5:fontfile=/usr/share/fonts/gnu-free/FreeSans.ttf:y=5:fontcolor=white:text='%%" +
    "{pts\:localtime\:%s}'\" -r 1 -f image2 -qscale:v 5 %s/img1%%03d.jpeg"
    )

    def __init__(self, path_to_video, db):
        """

        :param path_to_video:
        :param database.DBConnection db:
        """
        super(CutVideo, self).__init__()
        self.path_to_video = path_to_video
        self.db = db

        requires.logger.debug("CutVideo instance to '%s' path video" % self.path_to_video)

    def run(self):
        self.extract_frames()

    def extract_frames(self):
        self.databse_test()
        requires.logger.debug("Extracting frames from video '%s'" % self.path_to_video)

    def databse_test(self):
        requires.logger.debug(self.COMMAND);
        #self.db.testing_insert()
