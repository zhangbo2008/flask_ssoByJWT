DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_DB = 'flask-pyjwt-auth'

DEBUG = True
PORT = 3333
HOST = "127.0.0.1"
SECRET_KEY = "my blog"

SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DB
SQLALCHEMY_DATABASE_URI = 'sqlite:///dbdatabase.db'
