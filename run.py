from app import create_app
# debug走一遍流程还是必须的.
app = create_app('app.config')
# 创建表格、插入数据



# 初始化的部分都写这里就行了.

model={"初始化":"over"}


@app.route('/fun1', methods=['POST'])
def fun1():
    return model


if __name__ == '__main__':
    app.run(host=app.config['HOST'],
            port=app.config['PORT'],
            debug=app.config['DEBUG'])

