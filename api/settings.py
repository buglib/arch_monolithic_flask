import os

baseDir = os.path.abspath(__file__)


class AppConfig:
    # JSON序列化配置
    ENSURE_ASCII = False

    # OAUTH相关配置
    JWT_SIGNATURE_KEY = "601304E0-8AD4-40B0-BD51-0B432DC47461"
    OAUTH2_CLIENT_ID = "bookstore_frontend"
    OAUTH2_CLIENT_SECRET = "bookstore_secret"
    OAUTH2_ACCESS_TOKEN_EXPIRED_TIME = 3 * 60 * 60 * 1000
    OAUTH2_REFRESH_TOKEN_EXPIRED_TIME = 15 * 24 * 60 * 60 * 1000


class DevAppConfig(AppConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/bookstore"

    # 订单服务超时相关配置
    DEFAULT_PRODUCT_FROZEN_EXPIRES = 3


class TestAppConfig(AppConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/test_bookstore"

    # 订单服务超时相关配置
    DEFAULT_PRODUCT_FROZEN_EXPIRES = 3


class ProdAppConfig(AppConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://bookstore:bookstore@localhost:3306/bookstore"

    # 订单服务超时相关配置
    DEFAULT_PRODUCT_FROZEN_EXPIRES = 2 * 60


app_configs = dict(
    default=DevAppConfig,
    dev=TestAppConfig,
    test=TestAppConfig,
    prod=ProdAppConfig
)


# flask-caching相关配置
cache_config = dict(
    CACHE_TYPE = "FileSystemCache",
    CACHE_DEFAULT_TIMEOUT = 3 * 60,
    CACHE_DIR = "/Users/eassi/Deploments/arch_monolithic_flask/cache"
)


cache_configs = dict(
    default=cache_config,
    dev=cache_config,
    test=cache_config
)