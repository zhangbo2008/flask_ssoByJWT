from flask import jsonify, request
from app.users.model import Users
from app.auth.auths import Auth
from .. import common
# 这个定义了服务的所有service层!!!!!!!!!!

# 所以前段需要看这个文件!!!!!!!!!!!!!api


def init_api(app):
    @app.route('/register', methods=['POST'])
    def register():
        """
        用户注册
        :return: json
        """
        print(111111111111111,request)
        print(111111111111111,request.form.get('password'))
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users(email=email, username=username, password=Users.set_password(Users, password))  # 数据库中存的password是加密过后的,所以真是的password是不知道的.
        print(2222222222,user)
        print(333333333,user.id)
        result = Users.add(Users, user)
        if user.id:# 插入成功.
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }# common.trueReturn 就是进行字符串的封装一层.
            return jsonify(common.trueReturn(returnUser, "用户注册成功"))
        else:
            return jsonify(common.falseReturn('', '用户注册失败'))












    @app.route('/login', methods=['POST'])
    def login():
        """
        用户登录
        :return: json
        """
        username = request.form.get('username')
        password = request.form.get('password')
        if (not username or not password):
            return jsonify(common.falseReturn('', '用户名和密码不能为空'))
        else:
            return Auth.authenticate(Auth, username, password)










# 这个接口就是实际的例子:
    # 前段Authorization 这个字段里面需要协商token

    # head:  里面写上key Authorization  value:JWT token
    # 例子:JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODY5NTQzNDUsImlhdCI6MTU4NDM2MjMzNSwiaXNzIjoia2VuIiwiZGF0YSI6eyJpZCI6NiwibG9naW5fdGltZSI6MTU4NDM2MjMzNX19.lZesm6Ekxi3SURLQhgp95QTMIJ_k112zR4jj54RoZbU


    @app.route('/user', methods=['GET'])
    def get():
        """
        获取用户信息
        :return: json
        """
        result = Auth.identify(Auth, request)
        if (result['status'] and result['data']):
            user = Users.get(Users, result['data'])
            returnUser = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'login_time': user.login_time
            }
            result = common.trueReturn(returnUser, "请求成功")
        return jsonify(result)
