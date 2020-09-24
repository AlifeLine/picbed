# -*- coding: utf-8 -*-
"""
    utils.vars
    ~~~~~~~~~~

    :copyright: (c) 2020 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from .tool import rsp

#: username index key -> set
AK = rsp("accounts")

#: username detail key -> hash
UK = lambda username: rsp("account", username)

#: system config(admin site) key -> hash
SCK = rsp("config", "system")

#: hook plugins config -> hash(third_name: config)
HCK = rsp("config", "hook")

#: Hook state key -> set
HSK = rsp("config", "hookstate")

#: Hook third modules key -> set
HTK = rsp("config", "hookthirds")

#: Hook temp load time(every process) -> string
HLTK = rsp("config", "hookloadtime")
