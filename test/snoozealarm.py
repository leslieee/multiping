import os
import signal
import threading
import time

class SnoozeAlarm(threading.Thread):
    def __init__(self, zzz):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.zzz = zzz

    def run(self):
        time.sleep(self.zzz)
        os.kill(os.getpid(), signal.SIGALRM)

def snoozealarm(i):
    SnoozeAlarm(i).start()

class Timeout(Exception): pass

def raise_timeout(*args):
    raise Timeout()

def main():
    signal.signal(signal.SIGALRM, raise_timeout)
    snoozealarm(0.5)
    while True:
        time.sleep(0.05)
        print time.time()


if __name__ == '__main__':
    main()