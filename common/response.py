"""
# 规范接口返回body，每个接口都按照这个接口返回

    所有的接口返回http状态码均为200,具体业务代码见body返回体。
    status: 业务逻辑是否成功
    code: 替代了http状态码，比如code=201表示创建，code=403表示没有权限
    message: 返回对应的接口信息
    results: 返回api接口数据，其中result不一定是{},在get方法中会是[]

"""
body = {
    "status": "success",
    "code": 200,
    "message": "错误信息提示或业务信息返回",
    "results": {},
}
