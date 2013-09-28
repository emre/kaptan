# -*- coding: utf8 -*-
"""
    kaptan.handlers.dict_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

from . import BaseHandler


class DictHandler(BaseHandler):

    def load(self, data):
        return data

    def dump(self, data):
        return data
