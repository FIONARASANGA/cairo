import pathlib
import os
import sys

PACKAGE_ROOT = pathlib.Path(__file__).resolve().parent.parent


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SERVER_PORT = 5000


class ProductionConfig(Config):
    DEBUG = False
    SERVER_PORT = os.environ.get('PORT', 5000)


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
