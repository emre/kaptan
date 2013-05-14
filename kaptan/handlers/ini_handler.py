# -*- coding: utf8 -*-

import ConfigParser

from . import BaseHandler


class KaptanIniParser(ConfigParser.ConfigParser):

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


class IniHandler(BaseHandler):

    def load(self, file_):
        config = KaptanIniParser()
        config.read(file_)
        return config.as_dict()

    def dump(self, file_):
        raise NotImplementedError("Exporting .ini files is not supported.")
