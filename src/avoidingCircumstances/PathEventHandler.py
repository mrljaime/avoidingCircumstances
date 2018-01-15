from watchdog.events import PatternMatchingEventHandler
from avoidingCircumstances.CuttingVideo import CuttingVideo
import asyncio
import requires


class PathEventHandler(PatternMatchingEventHandler):

    patterns = ["*.xml", "*.lxml"]

    def __init__(self, loop):
        super().__init__()
        self.loop = loop

        requires.logger.debug("Initialize event handler object")

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

        if self.loop.is_running:
            requires.logger.debug("Before calling async function over EventLoop")
            asyncio.run_coroutine_threadsafe(self.doitAsync(event), loop=self.loop)
        else:
            requires.logger.error("EventLoop is not running.")
            raise

    def on_modified(self, event):
        self.process(event=event)

    def on_created(self, event):
        self.process(event=event)

    def on_deleted(self, event):
        self.process(event=event)

    async def doitAsync(self, event):
        # TODO: Get the name of the file and call to ffmpeg cli to cut the video to sending via ftp to seproban
        requires.logger.debug("On async function")
        cutVideo = CuttingVideo(event.src_path)
        cutVideo.execCommand()
