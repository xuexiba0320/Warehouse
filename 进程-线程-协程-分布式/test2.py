import threading
import time
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

"""
不要使用empty判断队列为空然后结束循坏，当put堵塞，get速度快的时候，队列只有一个
"""
que = Queue()


def put_data():
    for n in range(100):
        time.sleep(2)
        que.put(n)
        print(que.qsize(), f'存入数据{n}')


def get_data():
    data = que.get()
    time.sleep(0)
    print(f'【{data}】')


with ThreadPoolExecutor(max_workers=20) as executor:
    executor.submit(put_data)
    num = 0
    while True:
        # if not que.empty():
        executor.submit(get_data)
        # que.task_done()
        num += 1
        # else:
        #     break

print(num)