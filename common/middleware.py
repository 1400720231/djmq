from hashlib import md5

import redis
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings


class CheckSignMiddleware(MiddlewareMixin):
    """
        自定义中间件，实现签名认证拦截，用于在dispach之前的权限或者资质校验。
    """
    keys = ('appid', 'scheme', 'mode', 'source', 'target', 'sign_type', 'random_str', 'action', 'token', "sign")  # 必传的参数
    body = {
        "status": "success",
        "code": 200,
        "message": "签名校验成功",
        "result": ''  # token的值
    }

    def process_request(self, request):  # request就是当次请求的request对象
        # 检查必填参数是是否缺少

        for key in self.keys:
            if not request.POST.get(key, None):
                self.body.update({"status": "fail", "code": 400, "message": "缺少参数"})
                return JsonResponse(self.body)
        # 验证签名
        data = {key: request.POST.get(key) for key in self.keys}
        from_sign = data.pop('sign')
        token = data.pop("token")  # token不参与签名计算
        string = '&'.join(['%s=%s' % (k, v) for k, v in sorted(data.items())]) + '&key=%s' % '12345678'  # appkey暂时写死
        my_sign = md5(string.encode('utf-8')).hexdigest().upper()
        print(from_sign,my_sign)
        if not from_sign == my_sign:
            self.body.update({"status": "fail", "code": '403', "message": "签名校验失败，请核对文档。"})
            return JsonResponse(self.body)

        # 签名认证通过
        if token and data.get('action') == 'get':
            # 如果没有token 就生成一个token返回
            token = self.redis_conn('create')
            self.body.update({"result": token, "message": "获取token成功"})
            return JsonResponse(self.body)

        else:
            # 如果有token 验证token的真是性和有效期
            res = self.redis_conn('check', token)
            if not res:
                self.body.update({"success": "fail", "code": "403", "message": "token已经过期，请重新获取token"})
                return JsonResponse(self.body)
            # 返回None正常进入views
            return None

    def redis_conn(self, mode='create', token=''):
        conn = redis.StrictRedis.from_url(url=settings.API_TOKEN_URL, decode_responses=True)
        if mode == 'create':
            # 随机生成随机token,并且key的名字应该和分配的appid一样,这里写死为token
            conn.set('token', '123456', settings.API_TOKEN_EXPIRE)
            return "123456"
        else:
            if conn.get('token'):
                return True
            else:
                return False
