# -*- coding: utf8 -*-
"""
    kaptan.handlers.yaml_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import yaml

from . import BaseHandler


class YamlHandler(BaseHandler):

    def load(self, data, safe=True):
        if safe:
            func = yaml.safe_load
        else:
            func = yaml.load
        return func(data)

    def dump(self, data, safe=True, **kwargs):
        if safe:
            func = yaml.safe_dump
        else:
            func = yaml.dump
        return func(data, **kwargs)
