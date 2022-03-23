from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

# 定义一个准备作为线程任务的函数
def action(*arg):
    time.sleep(1)

    aa = threading.current_thread().name
    print(aa)
    return aa

# 创建一个包含2条线程的线程池
with ThreadPoolExecutor(max_workers=2) as pool:

    # future1 = [pool.submit(action) for i in range(55)]
    #
    # def get_result(future):
    #     time.sleep(0)
    #     print('***',future.result())
    # for n in future1:
    #     n.add_done_callback(get_result)
    # print('--------------')
    #

    results = pool.map(action, (1, 2, 3 ))
    print('++++++++')
    for i in results:
        print('-------',i)

