# -*- coding: utf8 -*-
import os

from collections import Mapping, Sequence

from handlers.json_handler import JsonHandler
from handlers.dict_handler import DictHandler
from handlers.yaml_handler import YamlHandler
from handlers.file_handler import FileHandler
from handlers.ini_handler import IniHandler


SENTINEL = object()

HANDLER_EXT = {
    'ini': 'ini',
    'conf': 'ini',
    'yaml': 'yaml',
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
                    self.handler = self.HANDLER_MAP[HANDLER_EXT.get(os.path.splitext(value)[1][1:], None)]()
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

    def get(self, key, default=SENTINEL):
        try:
            try:
                return self._get(key)
            except (KeyError):
                raise KeyError(key)
            except (ValueError):
                raise ValueError("Sequence index not an integer")
            except (IndexError):
                raise IndexError("Sequence index out of range")
        except (KeyError, ValueError, IndexError):
            if default is not SENTINEL:
                return default
            raise

    def export(self, handler=None):
        if not handler:
            handler_class = self.handler
        else:
            handler_class = self.HANDLER_MAP[handler]()

        return handler_class.dump(self.configuration_data)

    def __handle_default_value(self, key, default):
        if default == SENTINEL:
            raise KeyError(key)

        return default


def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(
        description='Configuration manager in your pocket')
    parser.add_argument('config_file', action='store',
                        help="file to load config from")
    parser.add_argument('--handler', action='store',
                        help="handler to use (default: guessed from filename)")
    parser.add_argument('-e', '--export', action='store', default='json',
                        help="format to export to")
    parser.add_argument('-k', '--key', action='store',
                        help="config key to get value of")
    args = parser.parse_args()
    handler = (
        args.handler or
        HANDLER_EXT.get(os.path.splitext(args.config_file)[1][1:], None)
    )
    if not handler:
        raise RuntimeError("Unable to determine handler")
    with open(args.config_file) as f:
        config = Kaptan(handler=handler)
        config.import_config(f.read())
    if args.key:
        print config.get(args.key)
    else:
        print config.export(args.export)
