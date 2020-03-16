import jwt, datetime, time
from flask import jsonify
from app.users.model import Users
from .. import config
from .. import common

class Auth():
    @staticmethod
    # 传入用户id,和当前时间. 返回加密后的cookie用的字符串 也就是token
    def encode_auth_token(user_id, login_time):
        """
        生成认证Token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        '''
        “exp”: 过期时间
        “nbf”: 表示当前时间在nbf里的时间之前，则Token不被接受
        “iss”: token签发者
        “aud”: 接收者
        “iat”: 发行时间
        '''
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',# 这个签名很重要,解密时候必须要用. 解密时候不写也能成功解密.
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
                algorithm='HS256'
            )# 返回一个bytes
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'





    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """

        # 这个去数据库中先搜索是不是存在.
        userInfo = Users.query.filter_by(username=username).first()
        if (userInfo is None):
            return jsonify(common.falseReturn('', '找不到用户'))
        else:
            if (Users.check_password(Users, userInfo.password, password)):
                login_time = int(time.time())
                userInfo.login_time = login_time
                # 更新了userInfo, 就是更新当前搜索到的用户的login_time.记录到数据库中.
                Users.update(Users)
                token = self.encode_auth_token(userInfo.id, login_time)
                return jsonify(common.trueReturn(token.decode(), '登录成功'))
            else:
                return jsonify(common.falseReturn('', '密码不正确'))

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        # 前段Authorization 这个字段里面需要协商token

        # head:  里面写上key Authorization  value:JWT token
        # 例子:JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY5NTQzNDUsImlhdCI6MTU4NDM2MjMzNSwiaXNzIjoia2VuIiwiZGF0YSI6eyJpZCI6NiwibG9naW5fdGltZSI6MTU4NDM2MjMzNX19.lZesm6Ekxi3SURLQhgp95QTMIJ_k112zR4jj54RoZbU
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr) != 2):
                result = common.falseReturn('', '请传递正确的验证头信息')
            else:
                auth_token = auth_tokenArr[1]
                payload = self.decode_auth_token(auth_token)

                # 从cookie中获取了payload
                if not isinstance(payload, str):
                    user = Users.get(Users, payload['data']['id'])
                    if (user is None):
                        result = common.falseReturn('', '找不到该用户信息')
                    else:# user 是数据库中的数据,
                        # 下面判断数据库中的login_time跟cookie中传过来的是不是一样的.
                        if (user.login_time == payload['data']['login_time']):
                            result = common.trueReturn(user.id, '请求成功')
                        else:
                            result = common.falseReturn('', 'Token已更改，请重新登录获取')
                else:
                    result = common.falseReturn('', payload)
        else:
            result = common.falseReturn('', '没有提供认证token')
        return result