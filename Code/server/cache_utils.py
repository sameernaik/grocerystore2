# cache_utils.py
from flask_caching import Cache

cache = Cache()


def init_cache(app, config=None):
    if config:
        app.config.from_mapping(config)
    cache.init_app(app)


def clear_cache():
    print('Clearing cache now')
    cache.clear()
