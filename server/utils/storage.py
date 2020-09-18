# -*- coding: utf-8 -*-
import json
from redis import Redis
from redis.client import list_or_args
from config import REDIS

__all__ = ["rc"]


def is_json(string):
    try:
        json.loads(string)
    except (ValueError, TypeError):
        return False
    else:
        return True


def json_dumps(obj):
    if obj is None:
        #: so raise DataError
        return obj
    return obj if is_json(obj) else json.dumps(obj)


def json_loads(obj):
    if not obj or not isinstance(obj, (str, bytes)):
        return obj
    try:
        return json.loads(obj)
    except ValueError:
        return obj


class MyRedis(Redis):
    '''Inherit and override certain methods to obtain native data types'''

    def set(self, name, value, **options):
        return super().set(name, json_dumps(value), **options)

    def get(self, name):
        return json_loads(super().get(name))

    def hset(self, name, key=None, value=None, mapping=None):
        if isinstance(mapping, dict):
            mapping = {k: json_dumps(v) for k, v in mapping.items()}
        return super().hset(
            name, key=key, value=json_dumps(value), mapping=mapping
        )

    def hget(self, name, key):
        return json_loads(super().hget(name, key))

    def hmset(self, name, mapping):
        return self.hset(name, mapping=mapping)

    def hmget(self, name, keys, *args):
        fields = list_or_args(keys, args)
        data = [json_loads(i) for i in super().hmget(name, keys, *args)]
        return dict(zip(fields, data))

    def hgetall(self, name):
        data = super().hgetall(name)
        return {k: json_loads(v) for k, v in data.items()}


def from_url(url, **kwargs):
    return MyRedis.from_url(url, **kwargs)


rc = from_url(REDIS, decode_responses=True)
