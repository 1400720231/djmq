# 内置包
import copy
import time
# 三方包
from django.views.generic.base import View
from django.http import JsonResponse
# utils
from common.response import body

# 项目代码
from apps.user.tasks import migrate


class TaskView(View):
    body = copy.deepcopy(body)

    def post(self, request):
        # migrate.delay()
        return JsonResponse(self.body)

    def get(self, request):
        # migrate.delay()
        return JsonResponse(self.body)
