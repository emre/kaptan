# -*- coding: utf8 -*-
"""
    kaptan.handlers.dict_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from . import BaseHandler


class DictHandler(BaseHandler):

    def load(self, data):
        return data

    def dump(self, data):
        return data
