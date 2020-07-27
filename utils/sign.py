
import rsa
import base64

# 随机成一对密钥，然后保存.pem格式文件,也可以直接使用
(pubkey, privkey) = rsa.newkeys(1024)
(pubkey2, privkey2) = rsa.newkeys(1024)
pub = pubkey.save_pkcs1()
print(pub.decode())
# pubfile = open('public.pem', 'w+', encoding='utf-8')
# pubfile.write(pub.decode())
# pubfile.close()

pri = privkey.save_pkcs1()
print(pri.decode())
# prifile = open('private.pem', 'w+')
# prifile.write(pri.decode())
# prifile.close()

# load公钥和密钥
message = 'abcdef'
print("原始字符串:", message)
# with open('public.pem') as publickfile:
#     p = publickfile.read()
#
#     pubkey = rsa.PublicKey.load_pkcs1(p)
#     print(pubkey)
# with open('private.pem') as privatefile:
#     p = privatefile.read()
#
#     privkey = rsa.PrivateKey.load_pkcs1(p)
#     print(privkey)

# 公钥加密(为了展示可以用base64编码)

crypto = base64.b64encode(rsa.encrypt(message.encode(), pubkey))
print(rsa.encrypt(message.encode(), pubkey))
print("rsa加密结果:", crypto)
# 私钥解密
from rsa.pkcs1 import DecryptionError
try:
    message = rsa.decrypt(base64.b64decode(crypto), privkey2)
except DecryptionError as e:
    print("签名认证失败")
print("rsa解密结果:", message)







# sign 用私钥签名
# signature = base64.b64encode(rsa.sign(message, privkey, 'SHA-1'))
# print("加签结果:", signature)
# # 再用公钥验证签名
# res = rsa.verify(message, base64.b64decode(signature), pubkey)
# print("验签结果:", res)
#

from alipay import AliPay