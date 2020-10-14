# -*- coding: utf-8 -*-
"""
    api.admin
    ~~~~~~~~

    Admin Interface

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from utils.exceptions import ApiError
from utils.vars import CTHK
from utils.storage import rc
from utils.web import try_proxy_request

class Admin():


    def list_third_hooks(self,
        page:int=1, limit:int=5, no_fresh:bool=True)->str:
        res = dict(code=1)
        try:
            page = int(page) - 1
            limit = int(limit)
            if page < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise ApiError("Parameter error")
        data = rc.get(CTHK)
        if no_fresh and data:
            res.update(code=0, data=data)
        else:
            url = "https://api.github.com/repos/{}/contents/{}".format(
                "staugur/picbed-awesome", "list.json",
            )
            headers = dict(Accept='application/vnd.github.v3.raw')
            try:
                r = try_proxy_request(url, headers=headers, method='GET')
                if not r.ok:
                    raise ValueError("Not Found")
            except (ValueError, Exception) as e:
                raise ApiError(str(e))
            else:
                data = r.json()
                res.update(code=0, data=data)
                rc.pipeline().set(CTHK, data).expire(CTHK, 3600 * 6).execute()
        if res["code"] == 0:
            def fmt(i, pkgs):
                pkg = i.get("pypi", "").replace("$name", i["name"])
                status = i.get("status")
                if status == "beta":
                    status_text = "公测版"
                elif status == "rc":
                    status_text = "预发布"
                elif status in ("stable", "production", "ga"):
                    status_text = "正式版"
                else:
                    status_text = ""
                if pkg:
                    pypi = "https://pypi.org/project/{}".format(pkg)
                else:
                    pypi = None
                user = i["github"].split("/")[0]
                i.update(
                    author=i.get("author", user),
                    home=i.get("home", "https://github.com/{}".format(user)),
                    github="https://github.com/{}".format(i["github"]),
                    pypi=pypi,
                    status_text=status_text,
                    pkg=dict(
                        name=pkg,
                        installed=pkg in pkgs,
                        local=pkgs.get(pkg),
                    ),
                )
                return i
            pkgs = _pip_list(fmt="dict", no_fresh=no_fresh)
            data = [
                fmt(i, pkgs)
                for i in res["data"]
                if isinstance(i, dict) and
                "name" in i and
                "module" in i and
                "desc" in i and
                "github" in i
            ]
            data.reverse()
            count = len(data)
            data = list_equal_split(data, limit)
            pageCount = len(data)
            if page < pageCount:
                res.update(
                    code=0,
                    count=count,
                    data=data[page],
                    pageCount=pageCount,
                )
            else:
                res.update(code=3, msg="No data")

    def get_latest_release(self):
        key = rsp("cache", "latestrelease")
        data = g.rc.get(key)
        if no_fresh and data:
            res.update(code=0, data=json.loads(data))
        else:
            url = "https://api.github.com/repos/staugur/picbed/releases/latest"
            try:
                r = try_proxy_request(url, method='GET')
                if not r.ok:
                    raise ValueError("Not Found")
            except (ValueError, Exception) as e:
                res.update(msg=str(e))
            else:
                fields = ["tag_name", "published_at", "html_url"]
                data = {k: v for k, v in iteritems(r.json()) if k in fields}
                res.update(code=0, data=data)
                pipe = g.rc.pipeline()
                pipe.set(key, json.dumps(data))
                pipe.expire(key, 3600 * 24)
                pipe.execute()
        if res["code"] == 0:
            res["show_upgrade"] = less_latest_tag(res["data"]["tag_name"])

