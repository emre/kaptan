# -*- coding: utf8 -*-

from handlers.json_handler import JsonHandler
from handlers.dict_handler import DictHandler
from handlers.yaml_handler import YamlHandler
from handlers.file_handler import FileHandler
from handlers.ini_handler import IniHandler


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

    def get(self, key):
        current_data = self.configuration_data
        for chunk in key.split('.'):
            try:
                current_data = current_data.get(chunk, {})
            except AttributeError as error:
                if isinstance(current_data, list):
                    try:
                        chunk = int(chunk)
                    except ValueError:
                        raise error

                    return current_data[chunk]
                else:
                    raise error

        return current_data

    def export(self, handler=None):
        if not handler:
            handler_class = self.handler
        else:
            handler_class = self.HANDLER_MAP[handler]()

        return handler_class.dump(self.configuration_data)

