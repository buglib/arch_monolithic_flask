import os

baseDir = os.path.abspath(__file__)


class Config:
    ENSURE_ASCII = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/test_bookstore"


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/bookstore"


configs = dict(
    default=TestConfig,
    dev=TestConfig,
    test=TestConfig,
    prod=ProdConfig
)