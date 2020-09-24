#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    cli
    ~~~

    Cli Entrance

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

import click
from redis.exceptions import RedisError
from werkzeug.security import generate_password_hash
from utils.storage import rc, is_json, json_loads
from utils.vars import SCK, HCK, HSK, HTK
from utils.tool import rsp, get_now, is_true


def echo(msg, color=None):
    click.echo(click.style(msg, fg=color))


def migrate1to2():
    '''migrate redis key format from v1 to v2'''
    from redis import from_url
    from config import REDIS
    orc = from_url(REDIS, decode_responses=True)
    nrc = rc
    pipe = nrc.pipeline()
    DATK = rsp('dat')
    for key in orc.keys():
        if key == DATK:
            continue
        if orc.type(key) == "string":
            kd = orc.get(key)
            if not is_json(kd):
                pipe.set(key, kd)
        elif orc.type(key) == "hash":
            data = orc.hgetall(key)
            for k, v in data.items():
                if not is_json(v):
                    pipe.hset(key, k, v)
    #: migrate picbed:dat
    DATD = orc.hgetall(DATK)
    if DATD and isinstance(DATD, dict):
        try:
            sc = json_loads(DATD.get("siteconfig"))
        except ValueError:
            sc = {}
        try:
            hs = json_loads(DATD.get("hookstate"))
        except ValueError:
            hs = []
        try:
            ht = json_loads(DATD.get("hookthirds"))
        except ValueError:
            ht = []
        for k, v in sc.items():
            pipe.hset(SCK, k, v)
        pipe.sadd(HSK, *hs)
        pipe.sadd(HTK, *ht)
        orc.delete(DATK)
    pipe.execute()


def exec_createuser(username, password, **kwargs):
    """创建账号"""
    return
    ak = rsp("accounts")
    username = username.lower()
    if rc.sismember(ak, username):
        echo("用户名已存在", "red")
    else:
        is_admin = kwargs.pop("is_admin", 0)
        uk = rsp("account", username)
        pipe = rc.pipeline()
        pipe.sadd(ak, username)
        if kwargs:
            pipe.hmset(uk, kwargs)
        pipe.hmset(uk, dict(
            username=username,
            password=generate_password_hash(password),
            is_admin=1 if is_true(is_admin) else 0,
            ctime=get_now(),
            status=1,
        ))
        try:
            pipe.execute()
        except RedisError as e:
            echo(e, "red")
        else:
            echo("注册成功！", "green")


if __name__ == "__main__":
    @click.group(context_settings={'help_option_names': ['-h', '--help']})
    def cli():
        pass

    @cli.command()
    @click.confirmation_option(prompt='Are you sure you want to upgrade?')
    @click.argument('v2v', type=click.Choice(['1to2']))
    def upgrade(v2v):
        """upgrade version(data format)"""
        #: 处理更新版本时数据迁移、数据结构变更、其他修改
        if v2v == '1to2':
            migrate1to2()

    @cli.command()
    @click.option('--HookLoadTime/--no-HookLoadTime', default=False)
    @click.option('--HookThirds/--no-HookThirds', default=False)
    @click.option('--InvalidKey/--no-InvalidKey', default=False)
    def clean(hookloadtime, hookthirds, invalidkey):
        """clean system cache/other"""
        if hookloadtime:
            s = get_storage()
            del s['hookloadtime']
        if hookthirds:
            s = get_storage()
            del s['hookthirds']
        if invalidkey:
            ius = rc.keys(rsp("index", "user", "*"))
            pipe = rc.pipeline()
            for uk in ius:
                us = rc.smembers(uk)
                for sha in us:
                    if not rc.exists(rsp("image", sha)):
                        pipe.srem(uk, sha)
            pipe.execute()

    @cli.command()
    @click.option('--username', '-u', type=str, required=True)
    @click.option('--password', '-p', type=str, required=True)
    @click.option('--nickname', '-n', type=str, default='')
    @click.option('--avatar', '-a', type=str, default='', help='avatar url')
    @click.option('--isAdmin/--no-isAdmin', default=False, show_default=True)
    def create(username, password, nickname, avatar, isadmin):
        """create user(admin)"""
        exec_createuser(
            username,
            password,
            is_admin=isadmin,
            avatar=avatar,
            nickname=nickname,
        )

    cli()
