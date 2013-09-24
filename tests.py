# -*- coding: utf8 -*-

"""
    kaptan
    ~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

import json
import os
import unittest

try:
    import yaml
except ImportError:
    yaml = None

import kaptan


sentinel = object()


class KaptanTests(unittest.TestCase):

    def __get_config_data(self):
        return {
            'debug': False,
        }

    def test_configuration_data(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertIn('debug', config.configuration_data)

    def test_main_get(self):
        config = kaptan.Kaptan()
        config.import_config({
            'show_comments': True,
            'entry_count': 10,
        })

        self.assertEqual(config.get("entry_count", 25), 10)
        self.assertEqual(config.get("entry_count"), 10)
        self.assertTrue(config.get("show_comments", None))
        self.assertTrue(config.get("show_comments", False))

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
        self.assertTrue(config.get('debug'))

    def test_default_dict_handler(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertFalse(config.configuration_data['debug'])

    def test_json_handler(self):
        config = kaptan.Kaptan(handler='json')
        config.import_config(json.dumps(self.__get_config_data()))

        self.assertTrue(config.get('debug'))

    def test_json_file_handler(self):
        json_file_name = os.tmpnam() + '.json'
        json_file = file(json_file_name, 'w')
        json_file.write("""
{"development": {
    "DATABASE_URI": "mysql://root:123456@localhost/posts"
  },
  "production": {
    "DATABASE_URI": "mysql://poor_user:poor_password@localhost/poor_posts"
  }
}
""")
        json_file.flush()

        config = kaptan.Kaptan(handler='json')
        config.import_config(json_file.name)
        self.assertEqual(
            config.get('production.DATABASE_URI'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    @unittest.skipIf(yaml is None, 'needs yaml')
    def test_yaml_handler(self):
        config = kaptan.Kaptan(handler='yaml')
        config.import_config(yaml.dump(self.__get_config_data()))
        self.assertFalse(config.get("debug"))

    @unittest.skipIf(yaml is None, 'needs yaml')
    def test_yaml_file_handler(self):
        yaml_file_name = os.tmpnam() + '.yaml'
        yaml_file = file(yaml_file_name, 'w')
        yaml_file.write("""
development:
    DATABASE_URI: mysql://root:123456@localhost/posts

production:
    DATABASE_URI: mysql://poor_user:poor_password@localhost/poor_posts
""")
        yaml_file.flush()

        config = kaptan.Kaptan(handler='yaml')
        config.import_config(yaml_file.name)
        self.assertEqual(
            config.get('production.DATABASE_URI'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    def test_ini_handler(self):
        value = """[development]
DATABASE_URI = mysql://root:123456@localhost/posts

[production]
DATABASE_URI = mysql://poor_user:poor_password@localhost/poor_posts
"""

        config = kaptan.Kaptan(handler='ini')
        config.import_config(value)

        self.assertEqual(
            config.get('production.database_uri'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    def test_ini_file_handler(self):
        ini_file_name = os.tmpnam()
        ini_file = file(ini_file_name, 'w')
        ini_file.write("""[development]
DATABASE_URI = mysql://root:123456@localhost/posts

[production]
DATABASE_URI = mysql://poor_user:poor_password@localhost/poor_posts
""")
        ini_file.flush()

        config = kaptan.Kaptan(handler='ini')
        config.import_config(ini_file.name)

        self.assertEqual(
            config.get('production.database_uri'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    def test_file_handler(self):
        temp_name = 'temp.py'

        try:
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
        finally:
            os.unlink(temp_name)

    def test_invalid_key(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertRaises(KeyError, config.get, 'invalidkey')
        self.assertRaises(KeyError, config.get, 'invaliddict.invalidkey')

    def test_invalid_key_with_default(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertEqual(config.get('invalid_key', 'default_value'), 'default_value')
        self.assertEqual(config.get('invalid_key.bar.baz', 'default_value'), 'default_value')

    def test_default_value_none(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertIsNone(config.get("invalid_key", None))
        self.assertIsNone(config.get("invalid_key.bar.baz", None))

    def test_get_all_config(self):
        config = kaptan.Kaptan()
        config.import_config(self.__get_config_data())

        self.assertIsInstance(config.get(), dict)
        self.assertIsInstance(config.get(''), dict)

if __name__ == '__main__':
    unittest.main()
