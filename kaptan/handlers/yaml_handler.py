# -*- coding: utf8 -*-
"""
    kaptan.handlers.yaml_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

import yaml
from . import BaseHandler


class YamlHandler(BaseHandler):

    def load(self, data):
        return yaml.load(data)

    def dump(self, data, **kwargs):
        return yaml.dump(data, **kwargs)
