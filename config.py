import os
import random, string


class Config(object):
    CSRF_ENABLED = True
    SECRET = ""
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_FOLDER = os.path.join(ROOT_DIR, "templates")
    APP = None
    SENDGRID_API_KEY = ""


class Developmentconfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 8000
    URL_MAIN = "http://%s:%s/" % (IP_HOST, PORT_HOST)
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = "localhost"
    PORT_HOST = 5000
    URL_MAIN = "http://%s:%s/" % (IP_HOST, PORT_HOST)
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    IP_HOST = "localhost"
    PORT_HOST = 8080
    URL_MAIN = "https://%s:%s/" % (IP_HOST, PORT_HOST)
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"


app_config = {
    "development": Developmentconfig(),
    "testing": TestingConfig(),
    "production": ProductionConfig(),
}

app_active = os.getenv("FLASK_ENV")
