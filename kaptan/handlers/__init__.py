# -*- coding: utf8 -*-


class BaseHandler(object):
    """
    Base class for data handlers.
    """

    def load(self, data):
        raise NotImplementedError

    def dump(self, data):
        raise NotImplementedError

