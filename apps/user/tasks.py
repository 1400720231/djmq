from celery import task

import time


@task
def migrade(rety):


    return {"messgae": "异步任务完成"}
