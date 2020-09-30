# -*- coding: utf-8 -*-
"""
    api.user
    ~~~~~~~~

    User Interface

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from werkzeug.security import check_password_hash, generate_password_hash
from utils.storage import rc
from utils.tool import is_true
from utils.web import check_username
from utils.exceptions import ApiError
from libs.mixins import UserMixin, EnDeMixin, ConfigMixin

class User(UserMixin, EnDeMixin, ConfigMixin):

    def register(self, username:str, password:str, ) -> dict:
        if username and password:
            if not check_username(username):
                raise ApiError(
                    "The username is invalid or registration is not allowed"
                )
            if len(password) < 6:
                raise ApiError("Password must be at least 6 characters")
            if self.has_user(username):
                raise ApiError("The username already exists")
            #: 用户状态 -1待审核 0禁用 1启用 -2审核拒绝(权限同-1)
            # 后台开启审核时默认是-1，否则是1
            # 禁用时无认证权限（无法登陆，无API权限）
            # 待审核仅无法上传，允许登录和API调用
            status = -1 if is_true(self.get_cfg("review")) else 1
            #: 参数校验通过，执行注册
            options = dict(
                        username=username,
                        password=generate_password_hash(password),
                        is_admin=0,
                        avatar=request.form.get("avatar") or "",
                        nickname=request.form.get("nickname") or "",
                        ctime=get_now(),
                        status=status,
                        label=g.cfg.default_userlabel,
            )
            uk = rsp("account", username)
            pipe = g.rc.pipeline()
            pipe.sadd(ak, username)
            pipe.hmset(uk, options)
            pipe.execute()
            res.update(code=0)
        else:
            raise ApiError("param error")
    