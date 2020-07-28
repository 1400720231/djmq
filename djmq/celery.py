"""
官方文档：
    https://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django

"""
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djmq.settings')
app = Celery('djmq')
# 从django的配置文件中读取celery的配置文件，并且规定相关参数都是以大写“CELERY”开头声明的
app.config_from_object('django.conf:settings', namespace='CELERY')
# 可重用应用程序的常见做法是在一个单独的tasks.py模块中定义所有任务，而Celery确实可以自动发现这些模块，
# 也就是在你的其他的app文件夹下面创建一个tasks.py文件来声明你的任务函数
app.autodiscover_tasks()


