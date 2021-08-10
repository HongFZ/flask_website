#encoding: utf-8
import os

#SECRET_KEY = os.urandom(24)
SECRET_KEY = 'hhhhhh'

DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'mysql980114'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'sufeoj'

# PERMANENT_SESSION_LIFETIME =

DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

TEACHER_USER_ID = 'caidateacher'
CMS_USER_ID = 'admcauda'

MAIL_SERVER = "smtp.sina.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
#MAIL_USE_SSL = True
MAIL_USERNAME = "huenx@sina.com"
MAIL_PASSWORD = "b1dab6b8f7a8d80a"
MAIL_DEFAULT_SENDER = "huenx@sina.com"


PER_PAGE = 15

UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'file_upload')