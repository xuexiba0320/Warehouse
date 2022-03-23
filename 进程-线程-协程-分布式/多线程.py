"""
from threading import Thread
"""

import time
from threading import Thread


def task(n):
    time.sleep(0.1)
    print(n)


def main():
    for n in range(100):  # 相当于开启了100个线程，消耗资源
        thread = Thread(target=task, args=(n,))
        thread.start()
        # thread.join()

    # start = True
    # a = 1
    # while start:
    #     thread = Thread(target=task, args=(a,))
    #     thread.start()
    #     a += 1
    #     if a > 100:
    #         break

def main2():
    for n in range(100):
        task(n)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    start2 = time.time()
    main2()
    end2 = time.time()
    print('多线程使用时间:', end-start, '单线程使用时间:', end2-start2)