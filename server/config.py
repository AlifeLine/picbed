# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~~

    The program configuration file, the preferred configuration item,
    reads the system environment variable first.

    :copyright: (c) 2019 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from os import getenv
from os.path import dirname, join, isfile


class Properties(object):
    '''read config from an ini file or environment'''

    def __init__(self, filename, from_env=False):
        self.filename = filename
        self.from_env = from_env
        self.properties = {}
        self._get_properties()

    def __get_dict(self, str_name, dict_name, value):
        if(str_name.find('.') > 0):
            k = str_name.split('.')[0]
            dict_name.setdefault(k, {})
            return self.__get_dict(str_name[len(k)+1:], dict_name[k], value)
        else:
            dict_name[str_name] = value
            return

    def _get_properties(self):
        if not isfile(self.filename):
            return
        with open(self.filename, 'Ur') as pro_file:
            for line in pro_file.readlines():
                line = line.strip().replace('\n', '')
                if line.find("#") != -1:
                    line = line[0:line.find('#')]
                if line.find('=') > 0:
                    strs = line.split('=')
                    strs[1] = line[len(strs[0])+1:]
                    self.__get_dict(
                        strs[0].strip(),
                        self.properties, strs[1].strip()
                    )
        return self.properties

    def get(self, k, default_value=None):
        if not self.properties:
            self._get_properties()
        v = self.properties.get(k)
        if self.from_env is True:
            if not v:
                v = getenv(k)
        return v or default_value


envs = Properties(join(dirname(__file__), ".cfg"), from_env=True)


GLOBAL = {

    "ProcessName": "picbed",
    # 自定义进程名(setproctitle)

    "Host": envs.get("picbed_host", "127.0.0.1"),
    # 监听地址

    "Port": int(envs.get("picbed_port", 9514)),
    # 监听端口

    "LogLevel": envs.get("picbed_loglevel", "DEBUG"),
    # 应用日志记录级别, 依次为 DEBUG, INFO, WARNING, ERROR, CRITICAL.

    "HookReloadTime": int(envs.get("picbed_hookreloadtime", 600)),
    # 钩子管理器默认重载时间，单位：秒

    "SecretKey": envs.get(
        "picbed_secretkey", "BD1E2CF7DF9CD6971D641C115EE72871BEDA2806"
    ),
    # Web应用固定密钥

    "MaxUpload": int(envs.get("picbed_maxupload", 20)),
    # 上传最大尺寸，单位MB
}


#: 存储核心数据，使用redis单实例，请开启AOF持久化!
REDIS = envs.get("picbed_redis_url")
# Redis数据库连接信息，格式:
# redis://[:password]@host:port/db
# host,port必填项,如有密码,记得密码前加冒号
#
# v1.6.0支持redis cluster集群连接，格式：
# rediscluster://host:port,host:port...


if __name__ == "__main__":
    from json import dumps
    print(dumps(
        {
            "global": GLOBAL,
            "redis": REDIS,
        },
        indent=4
    ))
