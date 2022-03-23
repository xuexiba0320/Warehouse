from multiprocessing import Process,Pool
import time
import os

def child_1(interval):
    print("子进程 (%s) 开始执行，父进程为 (%s)" % (os.getpid(), os.getppid()))
    t_start = time.time()
    time.sleep(interval)
    t_end = time.time()
    print("子进程 (%s) 执行时间为'%0.2f'秒" % (os.getpid(), t_end - t_start))

def child_2(interval):
    print("子进程 (%s) 开始执行，父进程为 (%s)" % (os.getpid(), os.getppid()))
    t_start = time.time()
    time.sleep(interval)
    t_end = time.time()
    print("子进程 (%s) 执行时间为'%0.2f'秒" % (os.getpid(), t_end - t_start))

if __name__ == '__main__':
    print("---父进程开始执行---")
    print("父进程 PID: %s" % os.getpid())
    pool = Process
    p1 = Process(target=child_1, args=(1,))
    p2 = Process(target=child_2, name="test", args=(2,))
    p1.start()
    p2.start()

    print("p1.is_alive = %s" % p1.is_alive())
    print("p2.is_alive = %s" % p2.is_alive())

    print("p1.name = %s" % p1.name)
    print("p1.pid = %s" % p1.pid)
    print("p2.name = %s" % p2.name)
    print("p2.pid = %s" % p2.pid)

    print("---等待子进程---")
    p1.join()
    p2.join()
    print("---父进程执行结束---")
