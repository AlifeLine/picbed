# -*- coding: utf-8 -*-
"""
    libs.mixins
    ~~~~~~~~~~~

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from base64 import urlsafe_b64decode
from utils.storage import rc
from utils.vars import AK, UK, SCK
from utils.tool import get_now, sha256
from utils._compat import text_type
from config import GLOBAL


class ConfigMixin():
    """System/hook config"""

    def get_cfgs(self) -> dict:
        '''system config(admin site)'''
        return rc.hgetall(SCK)

    def get_cfg(self, name: str) -> Any:
        '''fetch system config someone'''
        return rc.hget(SCK, name)


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

    def is_valid_cookie(self, sid: str = None) -> bool:
        '''Parse Login State(Authorization Cookie) with current SecretKey'''
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


class AdminMixin():
    """Admin Api"""
    pass
