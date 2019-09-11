from multiprocessing import Process
import random
import threading
from queue import Queue
from threading import Thread  # (2 класса "AB" учеников)
import time

class An:
    def __init__(self, text):
        self.text = text

    @staticmethod
    def f(text):
        a = []
        b = []
        with open(text) as f1:
            for name in f1:
                name = name.strip()
                if len(a)<=10 or len(b)<=10:
                    rand = random.randint(1,2)
                    if rand == 1:
                        a.append(name)
                    else:
                        b.append(name)
                else:
                    break
        print('В классе А:',a,'\n','В классе Б:',b)


class SearchName:
    def __init__(self, text):
        super().__init__()
        self.text = text

    def search(self, q):
        with open(self.text) as text1:
            for i in text1:
                q.put(i)
            q.put(None)
            q.put(None)

    @staticmethod
    def splitting(q, clas):
        while True:
            item = q.get()
            if item is None:
                break
            print(clas, item)


'''Процесс 3'''

class ReadText:
    def __init__(self, text):
        self.text = text

    def read_text(self):
        names = []
        with open(self.text) as file:
            for name in file:
                name = name.strip()
                names.append(name)
        return names

class SplitChild:
    def __init__(self, names):
        self._mutex = threading.RLock()
        self.names = names

    def f(self):
        self._mutex.acquire()
        random_class = []

        for name in self.names:
            self.names.remove(name)
            if len(random_class) < 10:
                random_class.append(name)
            else:
                break
        print('В ' + str(random.randint(1, 11)) + ' классе учатся:', random_class, '\n')
        self._mutex.release()
def main():

    t0 = time.time()
    p1 = Process(target=An.f, args=('a.txt',))
    '''Второй процесс'''

    t0 = time.time()
    q = Queue(2)
    A = Thread(target=SearchName.splitting, args=(q, "A class:"))
    B = Thread(target=SearchName.splitting, args=(q, "B class:"))

    '''Процесс 3'''
    t0 = time.time()

    text = ReadText('a.txt').read_text()

    childs = SplitChild(text)
    r = Thread(target=childs.f)
    r2 = Thread(target=childs.f)

    p1.start()
    A.start()
    B.start()
    r.start()
    r2.start()
    SearchName('a.txt').search(q)
    print('time:', time.time() - t0)
    A.join()
    p1.join()
    print('time:', time.time() - t0)
    B.join()
    r.join()
    r2.join()




if __name__ == '__main__':
    main()
