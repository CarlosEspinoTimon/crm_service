from collections import namedtuple
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = 'supersecretkey'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@db/app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    GOOGLE_PROJECT = os.environ.get('GOOGLE_PROJECT')
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL", None)
    Credentials = namedtuple('Credentials', 'id secret')
    OAUTH_CREDENTIALS = {
        'google': Credentials(
            os.environ.get("GOOGLE_CLIENT_ID", None),
            os.environ.get("GOOGLE_CLIENT_SECRET", None)
            ),
        'facebook': Credentials(
            os.environ.get("FACEBOOK_CLIENT_ID", None),
            os.environ.get("FACEBOOK_CLIENT_SECRET", None)
        )
    }


class Prod(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')


class Dev(Config):
    DEBUG = True
    HOST = "0.0.0.0"


class Test(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@db_test/test_db'
