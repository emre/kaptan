# -*- coding: utf8 -*-
"""
    kaptan.handlers.file_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

from . import BaseHandler


class FileHandler(BaseHandler):

    def load(self, file_):
        module = __import__(file_)
        data = dict()
        for key in dir(module):
            value = getattr(module, key)
            if not key.startswith("__"):
                data.update({key: value})
        return data

    def dump(self, file_):
        raise NotImplementedError("Exporting python files is not supported.")
