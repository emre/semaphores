
import random
import time

from threading import Thread, Semaphore


class Philosopher(Thread):

    def __init__(self, *args, **kwargs):
        self.index = kwargs.pop("index")
        self.forks = kwargs.pop("forks")
        self.multiplex = kwargs.pop("multiplex")

        super(Philosopher, self).__init__(*args, **kwargs)

    @property
    def left(self):
        return self.index % 5

    @property
    def right(self):
        # when it gets to 5, (4 + 1) % 5 = 0
        return (self.index + 1) % 5

    def think(self):
        time.sleep(0.1)

    def get_forks(self):
        self.multiplex.acquire()
        self.forks[self.left].acquire()
        print "{} got the left fork {}".format(self.index, self.left)
        self.forks[self.right].acquire()
        print "{} got the right fork {}".format(self.index, self.right)

    def eat(self):
        print "{} is eating.".format(self.index)
        time.sleep(random.random())

    def put_forks(self):
        self.forks[self.left].release()
        print "{} put the left fork {}".format(self.index, self.left)
        self.forks[self.right].release()
        print "{} put the right fork {}".format(self.index, self.right)
        self.multiplex.release()

    def run(self):
        while 1:
            self.think()
            self.get_forks()
            self.eat()
            self.put_forks()

            time.sleep(0.1)


def main():

    forks = [Semaphore(1) for i in xrange(5)]
    multiplex = Semaphore(4)  # make sure only 4 philoshopers eat concurrently

    for i in xrange(5):
        Philosopher(index=i, forks=forks, multiplex=multiplex).start()

if __name__ == '__main__':
    main()
