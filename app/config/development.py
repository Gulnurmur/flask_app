from .base import Config
from datetime import timedelta
import os

class Development(Config):

    SQLALCHEMY_DATABASE_URI = "postgres:///newflask"

    DEVELOPMENT = True
    ASSETS_DEBUG = True
    DEBUG = True
    JWT_SECRET_KEY = os.urandom(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes = 10)
    