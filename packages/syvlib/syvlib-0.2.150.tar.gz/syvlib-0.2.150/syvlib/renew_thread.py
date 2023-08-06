import threading
import time


class RenewThread(threading.Thread):

    def __init__(self, session):
        super(RenewThread, self).__init__()
        self.session = session
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        while True:
            for i in range(1800):
                if self.stop_event.is_set():
                    return
                time.sleep(1)
            self.session.renew()
