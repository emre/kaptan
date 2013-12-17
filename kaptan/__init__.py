# -*- coding: utf8 -*-
"""
    kaptan
    ~~~~~~

    configuration parser.

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import os
from collections import Mapping, Sequence

from .handlers.dict_handler import DictHandler
from .handlers.file_handler import FileHandler
from .handlers.ini_handler import IniHandler
from .handlers.json_handler import JsonHandler
from .handlers.yaml_handler import YamlHandler

SENTINEL = object()

HANDLER_EXT = {
    'ini': 'ini',
    'conf': 'ini',
    'yaml': 'yaml',
    'yml': 'yaml',
    'json': 'json',
    'py': 'file',
}


class Kaptan(object):

    HANDLER_MAP = {
        'json': JsonHandler,
        'dict': DictHandler,
        'yaml': YamlHandler,
        'file': FileHandler,
        'ini': IniHandler,
    }

    def __init__(self, handler=None):
        self.configuration_data = dict()
        self.handler = None
        if handler:
            self.handler = self.HANDLER_MAP[handler]()

    def upsert(self, key, value):
        self.configuration_data.update({key: value})
        return self

    def import_config(self, value):
        if not isinstance(value, dict) and os.path.isfile(value):
            if not self.handler:
                try:
                    key = HANDLER_EXT.get(os.path.splitext(value)[1][1:], None)
                    self.handler = self.HANDLER_MAP[key]()
                except:
                    raise RuntimeError("Unable to determine handler")
            with open(value) as f:
                value = f.read()
        elif isinstance(value, dict):  # load python dict
            self.handler = self.HANDLER_MAP['dict']()

        self.configuration_data = self.handler.load(value)
        return self

    def _get(self, key):
        current_data = self.configuration_data

        for chunk in key.split('.'):
            if isinstance(current_data, Mapping):
                current_data = current_data[chunk]
            elif isinstance(current_data, Sequence):
                chunk = int(chunk)

                current_data = current_data[chunk]
            else:
                # A scalar type has been found
                return current_data

        return current_data

    def get(self, key=None, default=SENTINEL):
        if not key:  # .get() or .get(''), return full config
            return self.export('dict')

        try:
            try:
                return self._get(key)
            except KeyError:
                raise KeyError(key)
            except ValueError:
                raise ValueError("Sequence index not an integer")
            except IndexError:
                raise IndexError("Sequence index out of range")
        except (KeyError, ValueError, IndexError):
            if default is not SENTINEL:
                return default
            raise

    def export(self, handler=None, **kwargs):
        if not handler:
            handler_class = self.handler
        else:
            handler_class = self.HANDLER_MAP[handler]()

        return handler_class.dump(self.configuration_data, **kwargs)

    def __handle_default_value(self, key, default):
        if default == SENTINEL:
            raise KeyError(key)
        return default


def main():
    import argparse
    from sys import stdin
    from collections import OrderedDict

    parser = argparse.ArgumentParser(
        prog=__package__,
        description='Configuration manager in your pocket')
    parser.add_argument('config_file', action='store', nargs='*',
                        help="file/s to load config from")
    parser.add_argument('--handler', action='store', default='json',
                        help="set default handler")
    parser.add_argument('-e', '--export', action='store', default='json',
                        help="set format to export to")
    parser.add_argument('-k', '--key', action='store',
                        help="set config key to get value of")
    args, ukargs = parser.parse_known_args()

    config = Kaptan()
    config_files = args.config_file + ukargs

    if not config_files:
        parser.print_help()
        parser.exit(1)

    def get_handlers():
        for f in config_files:
            s = f.split(':')
            if len(s) != 2:
                s += [None]
            yield tuple(s)

    config_handlers = OrderedDict(list(get_handlers()))

    for config_file, handler in config_handlers.items():
        is_stdin = config_file == '-'
        if is_stdin:
            handler = handler or args.handler
        else:
            ext = handler or os.path.splitext(config_file)[1][1:]
            handler = HANDLER_EXT.get(ext, args.handler)
        _config = Kaptan(handler=handler)
        if is_stdin:
            _config.import_config(stdin.read())
        else:
            with open(config_file) as f:
                _config.import_config(f.read())
        config.configuration_data.update(_config.configuration_data)

    if args.key:
        print(config.get(args.key))
    else:
        print(config.export(args.export))

    parser.exit(0)

