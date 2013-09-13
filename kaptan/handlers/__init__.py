# -*- coding: utf8 -*-
"""
    kaptan.handlers
    ~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

class BaseHandler(object):
    """
    Base class for data handlers.
    """

    def load(self, data):
        raise NotImplementedError

    def dump(self, data):
        raise NotImplementedError

