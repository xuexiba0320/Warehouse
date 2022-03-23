"""进程的使用
1、导入进程模块
2、创建子进程并指定执行任务
3、启动进程执行任务
"""

import multiprocessing  # 1、导入多进程模块
import time
import os


# 任务一
def task_1():
    for i in range(4):
        print('task_【1】:', i, '当前进程', os.getpid(), '父进程', os.getppid())
        time.sleep(0.1)


# 任务二
def task_2():
    for i in range(4):
        print('task_【2】:', i, '当前进程', os.getpid(), '父进程', os.getppid())
        time.sleep(0.5)


def not_process():
    start = time.time()
    task_1()
    task_2()
    end = time.time()
    print(f'单进程-单线程--程序运行时间总时长为:{end - start}秒')


def process():
    start = time.time()
    task_1_process = multiprocessing.Process(target=task_1)
    task_2_process = multiprocessing.Process(target=task_2)
    task_1_process.start()
    task_2_process.start()
    task_2_process.join()
    end = time.time()
    print(f'多进程-单线程--程序运行时间总时长为:{end - start}秒')


if __name__ == '__main__':
    not_process()
    process()
    # task_1 = multiprocessing.Process(target=not_process)
    # task_2 = multiprocessing.Process(target=not_process)
    # task_1.start()
    # task_2.start()
