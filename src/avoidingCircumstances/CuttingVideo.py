import os
import asyncio
import requires


class CuttingVideo:
    """
        CuttingVideo class allow
    """
    DEFAULT_COMMAND = "ffpmeg %s -i %s"

    def __init__(self, path_to_video):
        self.path_to_video = path_to_video
        self.loop = asyncio._get_running_loop()

        requires.logger.debug("CuttingVideo instance with '%s' path to video" % self.path_to_video)

    def execCommand(self):
        asyncio.run_coroutine_threadsafe(self.execCommandAsync(), loop=self.loop)

    async def execCommandAsync(self):
        requires.logger.debug("Executing command '%s'" % self.DEFAULT_COMMAND)