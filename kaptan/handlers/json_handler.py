# -*- coding: utf8 -*-
"""
    kaptan.handlers.json_handler
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import json

from . import BaseHandler


class JsonHandler(BaseHandler):

    def load(self, data):
        return json.loads(data)

    def dump(self, data, **kwargs):
        return json.dumps(data, **kwargs)
