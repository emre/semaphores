
import random
import time

from threading import Thread, Semaphore

queue = []


class Consumer(Thread):

    def __init__(self, *args, **kwargs):
        self.mutex = kwargs.pop("mutex")
        self.items = kwargs.pop("items")

        super(Consumer, self).__init__(*args, **kwargs)

    def run(self):
        while 1:
            self.items.acquire()
            self.mutex.acquire()
            print queue
            number = queue.pop(0)
            self.mutex.release()
            print "got the number", number

            time.sleep(0.1)


class Producer(Thread):

    def __init__(self, *args, **kwargs):
        self.mutex = kwargs.pop("mutex")
        self.items = kwargs.pop("items")

        super(Producer, self).__init__(*args, **kwargs)

    def run(self):

        while 1:

            self.mutex.acquire()
            queue.append(random.randint(0, 100))
            self.mutex.release()
            self.items.release()

            time.sleep(0.1)


def main():

    mutex = Semaphore(1)
    items = Semaphore(0)

    Producer(
        mutex=mutex,
        items=items
    ).start()

    Consumer(
        mutex=mutex,
        items=items
    ).start()

if __name__ == '__main__':
    main()
