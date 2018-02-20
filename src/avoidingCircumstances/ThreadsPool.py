import threading
import requires


class ThreadsPool:
    """
    Pool of workers
    """
    workers = []

    def __init__(self):
        self.lock = threading.Lock()
        requires.logger.info("WorkersPool created")

    def make_active(self, name):
        """
        Just to have control appending into stack

        :param name:
        :return:
        """
        with self.lock:
            self.workers.append(name)
            requires.logger.info("Append into workers pool with name '%s'" % name)

    def make_inactive(self, name):
        """"
        Remove name control on the stack

        :param name
        :return:
        """
        with self.lock:
            self.workers.remove(name)
            requires.logger.info("Remove from workers pool with name '%s'" % name)