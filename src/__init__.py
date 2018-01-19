import argparse
import time
from watchdog.observers import Observer
from avoidingCircumstances.PathEventHandler import PathEventHandler
import requires

parser = argparse.ArgumentParser(description="Cut video at frames and send it via FTP")
parser.add_argument("-rf", help="Path to read files", dest="rf", required=True)


if __name__ == "__main__":
    args = parser.parse_args()
    path = args.rf

    requires.config.add_section("runtime")
    requires.config.set("runtime", "path", path)

    """
        Watchdog shit
    """
    observer = Observer()
    observer.schedule(PathEventHandler(), path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(10)
    except ValueError as error:
        print(error)
    except KeyboardInterrupt:
        requires.logger.info("Cancel daemon by user")
        observer.stop()


    observer.join()