import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'supersecretkey'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@db/app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    GOOGLE_PROJECT = os.environ.get('GOOGLE_PROJECT')


class Prod(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class Dev(Config):
    DEBUG = True
    HOST = "0.0.0.0"


class Test(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@db_test/test_db'
