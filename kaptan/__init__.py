# -*- coding: utf8 -*-
from collections import Mapping, Sequence

from handlers.json_handler import JsonHandler
from handlers.dict_handler import DictHandler
from handlers.yaml_handler import YamlHandler
from handlers.file_handler import FileHandler
from handlers.ini_handler import IniHandler

SENTINEL = object()


SENTINEL = object()


class Kaptan(object):

    HANDLER_MAP = {
        'json': JsonHandler,
        'dict': DictHandler,
        'yaml': YamlHandler,
        'file': FileHandler,
        'ini': IniHandler,
    }

    def __init__(self, handler='dict'):
        self.configuration_data = dict()
        self.handler = self.HANDLER_MAP[handler]()

    def upsert(self, key, value):
        self.configuration_data.update({key: value})
        return self

    def import_config(self, value):
        self.configuration_data = self.handler.load(value)
        return self

# -*- coding: utf8 -*-
from collections import Mapping, Sequence

from handlers.json_handler import JsonHandler
from handlers.dict_handler import DictHandler
from handlers.yaml_handler import YamlHandler
from handlers.file_handler import FileHandler
from handlers.ini_handler import IniHandler


SENTINEL = object()


class Kaptan(object):

    HANDLER_MAP = {
        'json': JsonHandler,
        'dict': DictHandler,
        'yaml': YamlHandler,
        'file': FileHandler,
        'ini': IniHandler,
    }

    def __init__(self, handler='dict'):
        self.configuration_data = dict()
        self.handler = self.HANDLER_MAP[handler]()

    def upsert(self, key, value):
        self.configuration_data.update({key: value})
        return self

    def import_config(self, value):
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

    def export(self, handler=None):
        if not handler:
            handler_class = self.handler
        else:
            handler_class = self.HANDLER_MAP[handler]()

        return handler_class.dump(self.configuration_data)
