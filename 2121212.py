import jwt
import datetime



#  pyjwt的基本使用.
dic = {
    'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
    'iat': datetime.datetime.now(),  #  开始时间
    'iss': 'lianzong',  # 签名
    'data': {  # 内容，一般存放该用户id和开始时间
        'a': 1,
        'b': 2,
    },
}
# 下面的secret 2个是密钥,不写就没法编码解码.
s = jwt.encode(dic, 'secret', algorithm='HS256')  # 加密生成字符串
print(s)  # issuer 这个签名必须跟编码一致,不然就decode报错.
# 当然解密时候不写签名也可以.成功解密.
print(type(s))
s = jwt.decode(s, 'secret', issuer='lianzong', algorithms=['HS256'])  # 解密，校验签名
print(s)
print(type(s))