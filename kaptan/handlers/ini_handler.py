# -*- coding: utf8 -*-

import ConfigParser
import StringIO

from . import BaseHandler


class KaptanIniParser(ConfigParser.RawConfigParser):

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
        config.readfp(StringIO.StringIO(value))
        return config.as_dict()

    def dump(self, file_):
        raise NotImplementedError("Exporting .ini files is not supported.")
