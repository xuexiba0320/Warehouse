# 线程池和进程池的用法几乎一样 只用ProcessPoolExecutor改成ThreadPoolExecutor

from concurrent.futures import ProcessPoolExecutor
import os
import time
import random


def task(name):
    start_time = time.time()
    print('{} is running,  pid is {}'.format(name, os.getpid()))
    time.sleep(random.randint(1, 4))
    print('运行了{}秒'.format(time.time() - start_time))


if __name__ == '__main__':
    pool = ProcessPoolExecutor(max_workers=1)
    for x in range(10):
        pool.submit(task, 'dayu{}'.format(x))
    pool.shutdown(wait=True)  # 等待进程池任务结束  默认 wait=True
    print('主进程')