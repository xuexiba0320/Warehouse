import time
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

def my_job():
    print('my_job, {}'.format(time.ctime()))

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # 第一秒执行作业
    intervalTrigger=CronTrigger(second=1)

    # 每天的19:30:01执行作业
    # intervalTrigger=CronTrigger(hour=19, minute=30, second=1)

    # 每年的10月1日19点执行作业
    # intervalTrigger=CronTrigger(month=10, day=1, hour=19)

    scheduler.add_job(my_job, intervalTrigger, id='my_job_id')
    scheduler.start()