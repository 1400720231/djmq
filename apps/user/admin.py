from django.contrib import admin
from django_celery_beat.models import PeriodicTask, SolarSchedule, IntervalSchedule, ClockedSchedule, CrontabSchedule, \
    PeriodicTasks
from django_celery_results.models import TaskResult
# Register your models here.　

admin.register(PeriodicTask)
admin.register(SolarSchedule)
admin.register(IntervalSchedule)
admin.register(ClockedSchedule)
admin.register(CrontabSchedule)
admin.register(PeriodicTasks)
admin.register(TaskResult)