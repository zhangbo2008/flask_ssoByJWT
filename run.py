from app import create_app
# debug走一遍流程还是必须的.
app = create_app('app.config')
# 创建表格、插入数据

if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])

