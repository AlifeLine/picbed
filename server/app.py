# -*- coding: utf-8 -*-
"""
    app
    ~~~

    Entrance

    :copyright: (c) 2019 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from flask import Flask, g, request
from flask_jsonrpc import JSONRPC
from views import front_bp
from utils.tool import Attribute, is_true, parse_valid_comma, err_logger, \
    timestamp_to_timestring, raise_if_less_version
from utils.web import default_login_auth, change_userinfo
from libs.hook import HookManager
from config import GLOBAL

__author__ = 'staugur <staugur@saintic.com>'
__date__ = '2019-12-20'
__doc__ = 'Flask-based web self-built pictures bed'

#: require py3.6+
raise_if_less_version()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=GLOBAL["SecretKey"],
    MAX_UPLOAD=GLOBAL["MaxUpload"],
    MAX_CONTENT_LENGTH=GLOBAL["MaxUpload"] * 1024 * 1024,
    DOCS_BASE_URL="https://picbed.rtfd.vip",
    UPLOAD_FOLDER="upload",
)
jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)

jsonrpc.register_view_function(func)

hm = HookManager(app)
app.register_blueprint(front_bp)



@app.before_request
def before_request():
    g.rc = rc
    g.site = get_site_config()
    g.cfg = Attribute(g.site)
    g.signin, g.userinfo = default_login_auth()
    #: Trigger hook, you can modify flask.g
    hm.call("before_request")
    #: (Logged-on state)required field: username, is_admin
    g.userinfo = Attribute(change_userinfo(g.userinfo))
    g.is_admin = is_true(g.userinfo.is_admin)
    g.next = get_redirect_url()
    g.site_name = g.cfg.title_name or "picbed"
    g.hm = hm


@app.after_request
def after_request(res):
    #: Trigger hook, you can modify the response
    hm.call("after_request", _args=(res,))
    if g.cfg.cors:
        if g.cfg.cors == "*":
            res.headers.add("Access-Control-Allow-Origin", "*")
        else:
            cors = parse_valid_comma(g.cfg.cors)
            origin = request.headers.get("Origin")
            if origin in cors:
                res.headers.add("Access-Control-Allow-Origin", origin)
    res.headers['X-Content-Type-Options'] = 'nosniff'
    res.headers['X-Frame-Options'] = 'SAMEORIGIN'
    return res
