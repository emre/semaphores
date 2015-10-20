

from threading import Thread, Semaphore

import time

# shared count value
count = 0

def thread_finished(current_count=None):
    print "count:", current_count


class Incrementer(object):

    def __init__(self, mutex):
        self.mutex = mutex

    def run(self):
        global count

        self.mutex.acquire()
        new_count = count + 1

        # make a context switch on os job scheduler.
        time.sleep(0.001)

        count = new_count

        # callback to get current count value
        thread_finished(count)

        self.mutex.release()


def main():
    mutex = Semaphore(1)

    for i in xrange(10):
        Thread(target=Incrementer(mutex).run).start()


if __name__ == '__main__':
    main()
