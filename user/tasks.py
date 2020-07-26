from celery import task

import time


@task()
def testfunc():
    time.sleep(5)
    print('假设这里是异步耗时任务')
    return {"messgae": "异步任务完成"}

@task
def testfunc2():
    time.sleep(5)
    print('假设这里是异步耗时任务2')
    return {"messgae": "异步任务完成2"}


@task
def beattestfunc(x,y):
    print('假设这里是定时任务')
    print(x+y)
    return {"messgae": "定时任务完成"}
