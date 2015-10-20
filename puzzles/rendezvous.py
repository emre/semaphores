
"""
Think about rendezvous as a meeting point. Thread A and ThreadB should meet
before A2 and B2.

We want to guarantee that a1 happens before b2 and b1 happens before a2
"""

from threading import Thread, Semaphore


class ThreadA(object):

    def __init__(self, a_arrived, b_arrived):
        self.a_arrived = a_arrived
        self.b_arrived = b_arrived

    def run(self):

        print "A1"

        # release thread a arrival semaphore.
        self.a_arrived.release()

        # wait until thread b arrives.
        self.b_arrived.acquire()

        print "A2"


class ThreadB(object):

    def __init__(self, a_arrived, b_arrived):
        self.a_arrived = a_arrived
        self.b_arrived = b_arrived

    def run(self):

        print "B1"

        # release thread b arrival semaphore.
        self.b_arrived.release()

        # wait until thread a arrives.
        self.a_arrived.acquire()

        print "B2"


def main():
    a_arrived = Semaphore(0)
    b_arrived = Semaphore(0)

    t1 = ThreadA(a_arrived, b_arrived)
    t2 = ThreadB(a_arrived, b_arrived)

    Thread(target=t1.run).start()
    Thread(target=t2.run).start()


if __name__ == '__main__':
    main()
