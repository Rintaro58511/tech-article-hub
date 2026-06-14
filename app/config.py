class Config(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///tech_hub.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'secret_key'