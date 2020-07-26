from django.contrib import admin
from django.urls import path
from django.views.generic.base import View
from django.shortcuts import HttpResponse
from user.tasks import testfunc


class IndexView(View):
    def get(self, request):
        res = testfunc.delay() # 调用delay函数把任务放入celery
        print(res)
        print()
        return HttpResponse({"status": "success", "message": "首页访问成功"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', IndexView.as_view(), name='index')
]
