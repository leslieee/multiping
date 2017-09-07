import signal, time, threading, os

class Timeout():
  """Timeout class using ALARM signal"""
  class Timeout(Exception): pass

  class SnoozeAlarm(threading.Thread):
    def __init__(self, zzz):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.zzz = zzz

    def run(self):
        time.sleep(self.zzz)
        os.kill(os.getpid(), signal.SIGALRM)

  def __init__(self, sec):
    self.sec = sec

  def __enter__(self):
    signal.signal(signal.SIGALRM, self.raise_timeout)
    Timeout.SnoozeAlarm(self.sec).start()

  def __exit__(self, *args):
    signal.alarm(0) # disable alarm

  def raise_timeout(self, *args):
    raise Timeout.Timeout()

try:
    with Timeout(0.5):
        while True:
            time.sleep(0.1)
            print time.time()
except Timeout.Timeout:
    print "timeout"