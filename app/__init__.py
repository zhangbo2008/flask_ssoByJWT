from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users.model import Users

#  初始化写在了这里!!!!!!!!!!!!!!! 调用users里面的init函数.
def create_app(config_filename):
    print(
        __name__
    )
    app = Flask(__name__)
    app.config.from_object(config_filename)

    @app.before_first_request
    def create_db():
        # Recreate database each time for demo
        # db.drop_all()
        if Users.query.filter_by(id=1).first()==None:
        # print(11111111111111111111111,Users.query.filter_by(id=1).first())
        # print(22222222222222,Users.query.all())
        # tmp=Users.query.filter_by(id=0).first()
        # print(tmp)
            db.create_all()




            admin = Users('admin', "580312",'admin@example.com')
            db.session.add(admin)
            guestes = [Users('guest1', "580312",'guest1@example.com'),
                       Users('guest2', "580312",'guest2@example.com'),
                       Users('guest3', "580312",'guest3@example.com'),
                       Users('guest4', "580312",'guest4@example.com')]
            db.session.add_all(guestes)
            db.session.commit()
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response
    # 初始化数据库
    from app.users.model import db
    db.init_app(app)

    from app.users.api import init_api
    init_api(app)

    return app
