# -*- coding: utf8 -*-

from . import BaseHandler


class DictHandler(BaseHandler):

    def load(self, data):
        return data

    def dump(self, data):
        return data
