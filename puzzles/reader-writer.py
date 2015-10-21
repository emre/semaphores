
import time

from threading import Thread, Semaphore

reader_count = 0

FILE_TO_READ = "/tmp/file.txt"


class Writer(Thread):

    def __init__(self, *args, **kwargs):
        self.mutex = kwargs.pop("mutex")
        self.resource_empty = kwargs.pop("resource_empty")
        self.reader_id = kwargs.pop("reader_id")

        super(Writer, self).__init__(*args, **kwargs)

    def run(self):
        while 1:

            self.resource_empty.acquire()

            fd = open(FILE_TO_READ, "w+")
            fd.write("{}\n".format(self.reader_id))
            fd.close()

            self.resource_empty.release()

            time.sleep(0.5)


class Reader(Thread):

    def __init__(self, *args, **kwargs):
        self.mutex = kwargs.pop("mutex")
        self.resource_empty = kwargs.pop("resource_empty")

        super(Reader, self).__init__(*args, **kwargs)

    def run(self):
        global reader_count

        while 1:

            self.mutex.acquire()
            reader_count += 1
            if reader_count == 1:
                self.resource_empty.acquire()

            self.mutex.release()

            print "Reading file", open(FILE_TO_READ).read()

            self.mutex.acquire()
            reader_count -= 1
            if reader_count == 0:
                self.resource_empty.release()

            self.mutex.release()

            time.sleep(0.5)


def main():

    mutex = Semaphore(1)
    resource_empty = Semaphore(1)

    Writer(
        mutex=mutex,
        resource_empty=resource_empty,
        reader_id="1",
    ).start()

    Writer(
        mutex=mutex,
        resource_empty=resource_empty,
        reader_id="2",
    ).start()


    Reader(
        mutex=mutex,
        resource_empty=resource_empty
    ).start()

    Reader(
        mutex=mutex,
        resource_empty=resource_empty
    ).start()

    Reader(
        mutex=mutex,
        resource_empty=resource_empty
    ).start()

if __name__ == '__main__':
    main()
