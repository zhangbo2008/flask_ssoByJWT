from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from run import app
from app import db
# https://www.jb51.net/article/134068.htm   flask操作数据库
app.config.from_object('app.config')
'''
这个代码是操作数据库的.
'''
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
