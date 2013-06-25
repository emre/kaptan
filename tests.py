# -*- coding: utf8 -*-

import unittest
import kaptan

import json
import yaml
import os

sentinel = object()


class KaptanTests(unittest.TestCase):

    def setUp(self):
        pass

    def __get_config_data(self):
        return {
            'debug': False,
        }

    def test_configuration_data(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertEqual('debug' in config.configuration_data, True)

    def test_nested_configuration(self):
        config = kaptan.Kaptan()
        config.import_config({
            'pagination': {
                'per_page': 20,
                'limit': 5,
            }
        })

        self.assertEqual(config.get("pagination.limit"), 5)

    def test_lists_on_configuration(self):
        config = kaptan.Kaptan()
        config.import_config({
            'servers': ['redis1', 'redis2', 'redis3'],
        })

        self.assertEqual(config.get('servers.0'), 'redis1')

    def test_upsert(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertEqual(config.get('debug'), False)

        config.upsert('debug', True)
        self.assertEqual(config.get('debug'), True)

    def test_default_dict_handler(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertEqual(config.configuration_data["debug"], False)

    def test_json_handler(self):
        config = kaptan.Kaptan(handler='json')
        config.import_config(json.dumps(self.__get_config_data()))

        self.assertEqual(config.get("debug"), False)

    def test_yaml_handler(self):
        config = kaptan.Kaptan(handler='yaml')
        config.import_config(yaml.dump(self.__get_config_data()))
        self.assertEqual(config.get("debug"), False)

    def test_ini_handler(self):
        ini_file_name = os.tmpnam()
        ini_file = file(ini_file_name, "w")
        ini_file.write("""[development]
DATABASE_URI = mysql://root:123456@localhost/posts

[production]
DATABASE_URI = mysql://poor_user:poor_password@localhost/poor_posts
""")
        ini_file.flush()

        config = kaptan.Kaptan(handler='ini')
        config.import_config(ini_file.name)

        self.assertEqual(
            config.get("production.database_uri"),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    def test_file_handler(self):
        temp_name = 'temp.py'

        py_module = file(temp_name, 'w')
        py_module.write("""DATABASE = 'mysql://root:123456@localhost/girlz'
DEBUG = False
PAGINATION = {
    'per_page': 10,
    'limit': 20,
}
""")

        py_module.flush()

        config = kaptan.Kaptan(handler='file')
        config.import_config('temp')

        self.assertEqual(
            config.get("PAGINATION.limit"),
            20,
        )

        os.unlink(temp_name)

    def test_invalid_key(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertRaises(KeyError, config.get, 'invalidkey')
        self.assertRaises(KeyError, config.get, 'invaliddict.invalidkey')

    def test_invalid_key_with_default(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertEqual(config.get("invalid_key", 'default_value'), 'default_value')
        self.assertEqual(config.get("invalid_key.bar.baz", 'default_value'), 'default_value')

    def test_default_value_none(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertEqual(config.get("invalid_key", None), None)
        self.assertEqual(config.get("invalid_key.bar.baz", None), None)




