# -*- coding: utf8 -*-

import json
from . import BaseHandler


class JsonHandler(BaseHandler):

    def load(self, data):
        return json.loads(data)

    def dump(self, data, **kwargs):
        return json.dumps(data, **kwargs)
