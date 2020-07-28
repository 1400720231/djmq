from hashlib import md5
import requests
data = {
    "appid": "12345678",
    "scheme": "database",
    "mode": "create",
    "source": "dbname",
    "target": "dbbname2",
    "sign_type": "MD5",
    "random_str": "dsatfdasgdgasdasd09ueq",
    "action": "get",  # post表示添加任务，get表示获取task需要的动态token


}

src = '&'.join(['%s=%s' % (k, v) for k, v in sorted(data.items())]) + '&key=%s' % '12345678'

sign = md5(src.encode('utf-8')).hexdigest().upper()
data['sign'] = sign
data['token'] = '12345678'

