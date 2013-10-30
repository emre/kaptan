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

    def load(self, data):
        return yaml.load(data)

    def dump(self, data, safe=False, **kwargs):
        if not safe:
            return yaml.dump(data, **kwargs)
        else:
            return yaml.safe_dump(data, **kwargs)
