# 内置包
import copy
import time
# 三方包
from django.views.generic.base import View
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings
from django.http import JsonResponse
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# utils
from common.response import body


# 项目代码

# 添加任务
# class TaskViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     serializer_class = True
#     body = copy.deepcopy(body)
#
#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         return Response(self.body, status=status.HTTP_200_OK)
#


class TaskView(View):
    body = copy.deepcopy(body)

    def post(self, request):
        return JsonResponse(self.body)