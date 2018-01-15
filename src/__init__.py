import asyncio
from avoidingCircumstances.PathEventHandler import PathEventHandler
from watchdog.observers import Observer
import requires

if __name__ == "__main__":
    """
        Async stuff
    """
    loop = asyncio.get_event_loop()

    """
        Watchdog shit
    """
    observer = Observer()
    observer.schedule(PathEventHandler(loop=loop), path=".")
    observer.start()

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.stop()
        observer.stop()

    observer.join()