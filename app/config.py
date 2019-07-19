import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'supersecretkey'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@10.1.0.102/app_db'
    GOOGLE_LOGIN_CLIENT_ID = os.environ.get('GOOGLE_LOGIN_CLIENT_ID')
    GOOGLE_LOGIN_CLIENT_SECRET = os.environ.get('GOOGLE_LOGIN_CLIENT_SECRET')

    OAUTH_CREDENTIALS = {
            'google': {
                'id': GOOGLE_LOGIN_CLIENT_ID,
                'secret': GOOGLE_LOGIN_CLIENT_SECRET
            }
    }

    GOOGLE_PROJECT = os.environ.get('GOOGLE_PROJECT')
    GOOGLE_BUCKET = os.environ.get('GOOGLE_BUCKET')
    BUCKET_URL = 'https://storage.googleapis.com/crm-service-bucket/'

    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'


class Prod(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class Dev(Config):
    DEBUG = True


class Test(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@10.1.0.102/test_db'
