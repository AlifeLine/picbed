# -*- coding: utf-8 -*-
"""
    libs.mixins
    ~~~~~~~~~~~

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from base64 import urlsafe_b64decode, urlsafe_b64encode
from utils.storage import rc
from utils.vars import AK, UK, SCK, HCK
from utils.tool import get_now, sha256, hmac_sha256, generate_random
from utils._compat import text_type
from typing import Any
from config import GLOBAL


class ConfigMixin():
    """System/hook config"""

    def get_sys_cfgs(self) -> dict:
        '''system config(admin site)'''
        return rc.hgetall(SCK)

    def get_sys_cfg(self, name: str) -> Any:
        '''fetch system config someone'''
        return rc.hget(SCK, name)

    def set_sys_cfg(self, **mapping: dict) -> None:
        '''set system config'''
        if mapping and isinstance(mapping, dict):
            #: SCK format(hash):
            #: key -> form field name, value -> form field value
            rc.hmset(SCK, mapping)

    def get_hook_cfgs(self) -> dict:
        '''all hook config'''
        return rc.hgetall(HCK)

    def get_hook_cfg(self, hook_name: str) -> dict:
        '''hook config'''
        return rc.hget(HCK, hook_name)

    def set_hook_cfg(self, hook_name: str, **mapping: dict) -> None:
        '''set hook config'''
        if mapping and isinstance(mapping, dict):
            #: HCK format(hash):
            #: key -> hook name, value -> hook json data
            rc.hset(HCK, hook_name, mapping)


class UserMixin():
    """Common user api(not admin)"""

    def has_user(self, username: str) -> bool:
        pipe = rc.pipeline()
        pipe.sismember(AK, username).exists(UK(username))
        return pipe.execute() == [True, 1]

    def get_userinfo(self, username: str) -> dict:
        return rc.hmget(UK(username), (
            'username', 'is_admin', 'avatar', 'email',
            'nickname', 'ctime', 'status', 'token'
        ))

    def get_user_setting(self, username: str) -> dict:
        data = rc.hgetall(UK(username))
        return {k: v for k, v in data.items() if k.startswith("ucfg_")}


class EnDeMixin():
    """Encryption and decryption"""

    def gen_cookie(self, usr: str, max_age: int = 7200) -> str:
        '''Cookie string generated for temporary login'''
        expire = get_now() + max_age
        pwd = rc.hget(UK(usr), "password")
        sid = "%s.%s.%s" % (
            usr,
            expire,
            sha256("%s:%s:%s:%s" % (
                usr, pwd, expire, GLOBAL["SecretKey"]
            ))
        )
        return urlsafe_b64encode(sid.encode("utf-8")).decode("utf-8")

    def is_valid_cookie(self, sid: str = None) -> bool:
        '''Parse Login State(Authorization Cookie) for :meth:`gen_cookie`'''
        ok = False
        try:
            if not sid:
                raise ValueError
            sid = urlsafe_b64decode(sid)
            if not isinstance(sid, text_type):
                sid = sid.decode("utf-8")
            usr, expire, sha = sid.split(".")
            expire = int(expire)
        except (TypeError, ValueError, AttributeError, Exception):
            pass
        else:
            if expire > get_now():
                pwd = rc.hget(UK(usr), "password")
                if pwd and sha256(
                    "%s:%s:%s:%s" % (usr, pwd, expire, GLOBAL["SecretKey"])
                ) == sha:
                    ok = True
        return ok

    def is_valid_token(self):
        pass

    def gen_token(self, usr: str, token_secret_key: str) -> str:
        """Permanent token generated for Api login"""
        return urlsafe_b64encode(
            ("%s.%s.%s.%s" % (
                generate_random(),
                usr,
                get_now(),
                hmac_sha256(token_secret_key, usr)
            )).encode("utf-8")
        ).decode("utf-8")


class AdminMixin():
    """Admin Api"""
    pass
