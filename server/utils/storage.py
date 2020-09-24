# -*- coding: utf-8 -*-
"""
    utils.storage
    ~~~~~~~~~~~~~

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

import json
from typing import Any, Mapping
from redis import Redis
from redis.client import list_or_args, Pipeline
from config import REDIS

__all__ = ["rc"]


def is_json(string) -> bool:
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

    def set(self, name: str, value: Any, **options) -> bool:
        '''json set'''
        return super().set(name, json_dumps(value), **options)

    def get(self, name: str) -> Any:
        '''json get'''
        return json_loads(super().get(name))

    def hset(
        self,
        name: str,
        key: str = None,
        value: Any = None,
        mapping: Mapping = None
    ) -> int:
        '''json hset'''
        if isinstance(mapping, dict):
            mapping = {k: json_dumps(v) for k, v in mapping.items()}
        return super().hset(
            name, key=key, value=json_dumps(value), mapping=mapping
        )

    def hget(self, name: str, key: str) -> Any:
        '''json hget'''
        return json_loads(super().hget(name, key))

    def hmset(self, name: str, mapping: Mapping) -> int:
        '''json hmset'''
        return self.hset(name, mapping=mapping)

    def hmget(self, name: str, keys: str, *args) -> dict:
        '''json hmget'''
        fields = list_or_args(keys, args)
        data = [json_loads(i) for i in super().hmget(name, keys, *args)]
        return dict(zip(fields, data))

    def hgetall(self, name: str) -> dict:
        '''json hgetall'''
        data = super().hgetall(name)
        return {k: json_loads(v) for k, v in data.items()}

    def pipeline(self, transaction=True, shard_hint=None):
        '''custom pipeline'''
        return MyPipeline(
            self.connection_pool,
            self.response_callbacks,
            transaction,
            shard_hint)


class MyPipeline(Pipeline, MyRedis):
    '''Execute write command with MyRedis'''

    def hmget(self, *args, **kwargs):
        raise RuntimeError("DENY")

    hgetall = hmget


def from_url(url, **kwargs):
    return MyRedis.from_url(url, **kwargs)


rc = from_url(REDIS, decode_responses=True)
