from flask import Flask
from flask_caching import Cache

from ...settings import cache_configs


cache = Cache()


def register_cache(cache: Cache, app: Flask, config_name: str = "default") -> Cache:
    cache.init_app(app=app, config=cache_configs[config_name])