"""
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
"""

import time
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
import queue


def task(n):
    time.sleep(2)
    print(n)
    return n


def result(data):
    time.sleep(0.5)
    print('结果:',data)

def main():
    que = queue.Queue()
    with ThreadPoolExecutor(max_workers=120) as executor:
        a = {executor.submit(task, n):n for n in range(1000)}
        que.put(a)
        b = que.get()
        [executor.submit(result, a[i]) for i in as_completed(b)]




def main2():
    for n in range(100):
        task(n)


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time()
    # start2 = time.time()
    # main2()
    # end2 = time.time()
    # print('多线程使用时间:', end-start, '单线程使用时间:', end2-start2)
    print('多线程使用时间:', end-start)