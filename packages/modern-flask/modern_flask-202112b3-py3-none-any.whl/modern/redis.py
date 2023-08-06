import json
from functools import wraps

import redis
from flask import Flask, g
from opentelemetry.instrumentation.redis import RedisInstrumentor
from redis import Redis


def redis_client() -> redis.Redis:
    return g.redis_client


def redis_cached(ex: int = 10, *keys):
    """
    decorate a function with redis cache with JSON serialization
    :param ex: expiration in seconds
    :param keys: cache keys, will be composed with dot
    :return:
    """

    def wrapper_builder(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cache_key = "cache." + ".".join([str(key) for key in keys])
            raw = redis_client().get(cache_key)
            if raw is None:
                ret = f(*args, **kwargs)
                redis_client().set(cache_key, json.dumps(ret), ex=ex)
                return ret
            return json.loads(raw)

        return wrapper

    return wrapper_builder


def redis_synchronized(*lock_args, **lock_kwargs):
    """
    decorate a function with redis_client.lock
    :param lock_args:
    :param lock_kwargs:
    :return:
    """

    def wrapper_builder(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with redis_client().lock(*lock_args, **lock_kwargs):
                return f(*args, **kwargs)

        return wrapper

    return wrapper_builder


def setup_redis(app: Flask):
    RedisInstrumentor().instrument()

    args = app.config.get_namespace("REDIS_")
    client = Redis(**args)

    @app.before_request
    def do_before_request():
        g.redis_client = client
