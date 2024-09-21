import pathlib


BASE_DIR = pathlib.Path(__file__).parent


class Config:
    SECRET_KEY = '1234567890'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/site.db'
