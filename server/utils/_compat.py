# -*- coding: utf-8 -*-
"""
    utils._compat
    ~~~~~~~~~~~~~

    A module providing tools for cross-version compatibility.

    :copyright: (c) 2019 by staugur.
    :license: BSD 3-Clause, see LICENSE for more details.
"""

from sys import version_info as vs
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urlparse, urlsplit, parse_qs

PY2 = vs[0] == 2
text_type = str
string_types = (str, )
integer_types = (int, )


def iteritems(d):
    return iter(d.items())


def itervalues(d):
    return iter(d.values())
