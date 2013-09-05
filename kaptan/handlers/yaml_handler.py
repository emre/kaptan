# -*- coding: utf8 -*-

import yaml
from . import BaseHandler


class YamlHandler(BaseHandler):

    def load(self, data):
        return yaml.load(data)

    def dump(self, data, **kwargs):
        return yaml.dump(data, **kwargs)
