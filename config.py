import os


class BaseConfig(object):
    SECRET_KEY = "5n)5wm0-u7v2us+)bdg*g@_%_8e&xw5otvh&u&du_z87%(4+)+"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    FLASK_ENV = ENV = os.getenv('FLASK_ENV', 'production')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_NAME = f'{FLASK_ENV}-storage.db' if FLASK_ENV != 'production' else 'storage.db'
    SQLALCHEMY_DATABASE_URL = (
        'sqlite:///' + os.path.join(BASE_DIR, f"databases/{DB_NAME}"),
    )
    SQLALCHEMY_BINDS = {
        'brazil': 'sqlite:///' + os.path.join(BASE_DIR, f"databases/br-{DB_NAME}"),
        'europe': 'sqlite:///' + os.path.join(BASE_DIR, f"databases/eu-{DB_NAME}"),
    }


class Development(BaseConfig):
    DEBUG = True


class Production(BaseConfig):
    pass


class Testing(BaseConfig):
    TESTING = True
