import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from subprocess import Popen


class _Handler(FileSystemEventHandler):
    def __init__(self):
        super()
        self._now = time.time() - 10.0
        self._start()

    def _start(self):
        self._proc = Popen(['bin/apimail'])

    def on_any_event(self, event):
        if time.time() - self._now < 2:
            return None
        self._now = time.time()

        if event.is_directory:
            return None

        self._proc.terminate()
        self._start()


def main():
    observer = Observer()
    event_handler = _Handler()
    observer.schedule(event_handler, 'mail/api', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
