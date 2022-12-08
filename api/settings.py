import os

baseDir = os.path.abspath(__file__)


class Config:
    ENSURE_ASCII = False
    JWT_SIGNATURE_KEY = "601304E0-8AD4-40B0-BD51-0B432DC47461"
    OAUTH2_CLIENT_ID = "bookstore_frontend"
    OAUTH2_CLIENT_SECRET = "bookstore_secret"
    OAUTH2_ACCESS_TOKEN_EXPIRED_TIME = 3 * 60 * 60 * 1000
    OAUTH2_REFRESH_TOKEN_EXPIRED_TIME = 15 * 24 * 60 * 60 * 1000


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/bookstore"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/test_bookstore"


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/bookstore"


configs = dict(
    default=DevConfig,
    dev=TestConfig,
    test=TestConfig,
    prod=ProdConfig
)