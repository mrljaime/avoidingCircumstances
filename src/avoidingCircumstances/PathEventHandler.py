# coding=utf-8

from watchdog.events import PatternMatchingEventHandler
from avoidingCircumstances.CutVideo import CutVideo
from database.DBConnection import DBConnection
import requires


class PathEventHandler(PatternMatchingEventHandler):

    patterns = ["*.avi"]
    ignore_patterns = ["*.log"]
    ignore_directories = False

    """
    Database connection
    """
    cnx = None

    def __init__(self):
        super(PathEventHandler, self).__init__()
        self.cnx = DBConnection(host=requires.config.get("db", "host"),
                                port=requires.config.getint("db", "port"),
                                username=requires.config.get("db", "username"),
                                password=requires.config.get("db", "password"),
                                database=requires.config.get("db", "database"))

        requires.logger.debug("Initialize event handler object")
        requires.logger.debug(requires.config.get("runtime", "path"))

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        requires.logger.debug("On process with source path '%s' on event '%s'" % (event.src_path, event.event_type))

        cutVideo = CutVideo(event.src_path, self.cnx)
        cutVideo.start()

#        if self.loop.is_running:
#            requires.logger.debug("Before calling async function over EventLoop")
#            asyncio.run_coroutine_threadsafe(self.doitAsync(event), loop=self.loop)
#        else:
#            requires.logger.error("EventLoop is not running.")
#            raise

    def on_modified(self, event):
        self.process(event=event)

    def on_created(self, event):
        self.process(event=event)

    def on_deleted(self, event):
        self.process(event=event)