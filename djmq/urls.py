# 内置包

# 三方包
from django.contrib import admin
from django.urls import path
from django.conf import settings


# 自定义公共组件


# 业务代码
from apps.user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 所以api接口
    path('task',user_views.TaskView.as_view(), name='task')

]
