
import os

from dotenv import load_dotenv
from flask_sslify import SSLify


# Load environment variables.
load_dotenv('.env')


class Config:

    SECRET_KEY = os.environ['SECRET_KEY']
    SESSION_COOKIE_SECURE = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    pass


class ProductionConfig(Config):

    @staticmethod
    def init_app(app):
        SSLify(app=app)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
