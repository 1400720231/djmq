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


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
"""
采用原生celery形式配置，并没有采用django_celery方式，按照文档走就行
需要主要的有几点：
    django1.8之后文档建议celery4.0之后，有时候确实会遇到奇怪的问题，所以一定要按规范走
    app.config_from_object('django.conf:settings', namespace='CELERY')设置表示所有相关参数以CELERY开头，
        我刚开始没有设置把BROKEN_URL变成CELERY_BROKEN_URL导致报错连不上rabbitmq，但是我声明的是redis作为消息队列中间建，
        因为没有捕捉到CELERY_BROKEN_URL所以默认就去找rabbitmq端口5672连


类似django的python manage.py runserver的本地启动命令

celery -A proj worker -l info
 

celery -A djmq.celery worker -l info
celery -A djmq.celery beat -l info  --scheduler django_celery_beat.schedulers:DatabaseScheduler
flower -A djmq.celery -l info

默认情况下redis /0 库中有个key名叫做“celery”的list保存了task相关信息，如uuid等：
{'body': 'W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=',
 'content-encoding': 'utf-8',
 'content-type': 'application/json',
 'headers': {'argsrepr': '()',
             'eta': None,
             'expires': None,
             'group': None,
             'id': 'c6f7f825-3a0e-4706-b73d-8ddd1b706162',
             'kwargsrepr': '{}',
             'lang': 'py',
             'origin': 'gen15343@GE60',
             'parent_id': None,
             'retries': 0,
             'root_id': 'c6f7f825-3a0e-4706-b73d-8ddd1b706162',
             'shadow': None,
             'task': 'user.tasks.testfunc',
             'timelimit': [None, None]},
 'properties': {'body_encoding': 'base64',
                'correlation_id': 'c6f7f825-3a0e-4706-b73d-8ddd1b706162',
                'delivery_info': {'exchange': '', 'routing_key': 'celery'},
                'delivery_mode': 2,
                'delivery_tag': '2f6920e5-3da0-4c4c-abb3-9dc505b96c57',
                'priority': 0,
                'reply_to': 'b9d227ed-16df-3ebf-8a8d-e74dc8f9d9ed'}}
如果配置了自己的routes 任务的分配的队列就会变化，也就是redis的list的key会变化
{'body': 'W1tdLCB7fSwgeyJjYWxsYmFja3MiOiBudWxsLCAiZXJyYmFja3MiOiBudWxsLCAiY2hhaW4iOiBudWxsLCAiY2hvcmQiOiBudWxsfV0=',
 'content-encoding': 'utf-8',
 'content-type': 'application/json',
 'headers': {'argsrepr': '()',
             'eta': None,
             'expires': None,
             'group': None,
             'id': 'e7c6c752-d99d-4068-b8d3-eaecec204dbc',
             'kwargsrepr': '{}',
             'lang': 'py',
             'origin': 'gen15441@GE60',
             'parent_id': None,
             'retries': 0,
             'root_id': 'e7c6c752-d99d-4068-b8d3-eaecec204dbc',
             'shadow': None,
             'task': 'user.tasks.testfunc',
             'timelimit': [None, None]},
 'properties': {'body_encoding': 'base64',
                'correlation_id': 'e7c6c752-d99d-4068-b8d3-eaecec204dbc',
                'delivery_info': {'exchange': '', 'routing_key': 'sqllog'},
                'delivery_mode': 2,
                'delivery_tag': '1efd7b16-d8de-44c0-92b5-7f297d4fbd5a',
                'priority': 0,
                'reply_to': '562ec184-cc7c-3cbc-8cd2-bbd6347fddd6'}}



"""