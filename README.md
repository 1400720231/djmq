# 下载项目
```shell script

git clone https://github.com/1400720231/djmq.git
pip install -i https://pypi.douban.com/simple -r requirements.txt
```
#安装需要的数据库
```shell script

mysql或者psql
redis
```
>其中redis 0库作为中间broker，是否有其他项目在用0库
# 安装nginx,具体配置文件见deploy文件夹
```shell script

upstream djmq {

  server 127.0.0.1:8000; # for a web port socket (we'll use this first)
}
# configuration of the server

server {

  listen      80;  # 监听端口
  server_name  10.10.8.103; # 绑定域名或者ip,比如你主机的ip

  charset     utf-8;

  client_max_body_size 75M;   # adjust to taste


  location /static {
    alias /home/python/all_envs/djmq_env/djmq/staticfiles; # 指向django的static目录
  }

  # Finally, send all non-media requests to the Django server.
  location / {
    uwsgi_pass  djmq;
    include uwsgi_params; # the uwsgi_params file you installed
  }
}

nginx -s relaod
```
#确保setting.py中的数据库账号密码正确
```shell script

python manage.py migrate # 迁移数据库结构
```
#收集django 静态文件
```shell script
python manage.py collectstatic
```
# 创建超级用户
```shell script
python manage.py createsuperuser
```
#django以配置文件方式项目启动

```shell script
[uwsgi]

# Django-related settings
# the base directory (full path)　项目目录
chdir = /home/python/all_envs/djmq_env/djmq
# Django's wsgi file　django项目wsgi文件路径
module = djmq.wsgi
# the virtualenv (full path)

# process-related settings
# master　开启主进程
master = true
# maximum number of worker processes　4
processes = 4
pidfile = /tmp/djmq.pid
max-requests = 5000
# the socket (use the full path to be safe　8000端口
socket = 127.0.0.1:8000
# with appropriate permissions - may be needed
# chmod-socket    = 664
# clear environment on exit
vacuum = true
# 虚拟环境,bin目录的上一层
virtualenv = /home/python/all_envs/djmq_env
# 日志文件目录|配置此选项后看不到终端输出，输出会在djmq.log中
logto = /tmp/djmq.log
;buffer-size  = 819200

```
>uwsgi -i uwsgi.ini　＆

# 异步任务启动(可以考虑用supervisor)
```shell script
nohup celery -A djmq.celery worker -l info &
```

# 定时任务启动(可以考虑用supervisor)
```shell script

nohup celery -A djmq.celery beat -l info  --scheduler django_celery_beat.schedulers:DatabaseScheduler &

```

