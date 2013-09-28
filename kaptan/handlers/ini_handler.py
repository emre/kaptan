# -*- coding: utf8 -*-
"""
    kaptan.handlers.ini_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

try:
    import ConfigParser as configparser
    from StringIO import StringIO

    configparser.RawConfigParser.read_file = configparser.RawConfigParser.readfp
except ImportError:  # Python 3
    import configparser
    from io import StringIO

from . import BaseHandler


class KaptanIniParser(configparser.RawConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class IniHandler(BaseHandler):

    def load(self, value):
        config = KaptanIniParser()
        # ConfigParser.ConfigParser wants to read value as file / IO
        config.read_file(StringIO(value))
        return config.as_dict()

    def dump(self, file_):
        raise NotImplementedError("Exporting .ini files is not supported.")
