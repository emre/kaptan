# -*- coding: utf8 -*-

"""
    kaptan
    ~~~~~~

    :copyright: (c) 2013 by the authors and contributors (See AUTHORS file).
    :license: BSD, see LICENSE for more details.
"""

from __future__ import print_function, unicode_literals

import json
import os
import sys
import os.path
import tempfile
try:
    import unittest2 as unittest  # for Python 2.6
except ImportError:
    import unittest

try:
    import yaml
except ImportError:
    yaml = None

import kaptan

# python 2/3 compat
try:
    unicode = unicode
except NameError:
    # py changes unicode => str
    unicode = str

PY2 = sys.version_info[0] == 2


sentinel = object()


class KaptanTests(unittest.TestCase):

    def setUp(self):
        self.config = {
            'debug': False,
        }

    def test_configuration_data(self):
        config = kaptan.Kaptan()
        config.import_config(self.config)

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
        config.import_config(self.config)

        self.assertEqual(config.get('debug'), False)

        config.upsert('debug', True)
        self.assertTrue(config.get('debug'))

    def test_default_dict_handler(self):
        config = kaptan.Kaptan()
        config.import_config(self.config)

        self.assertFalse(config.configuration_data['debug'])

    def test_json_handler(self):
        config = kaptan.Kaptan(handler='json')
        config.import_config(json.dumps(self.config))

        self.assertFalse(config.get('debug'))

    def test_json_file_handler(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json',
                                         delete=False) as fobj:
            fobj.write("""{"development": {
    "DATABASE_URI": "mysql://root:123456@localhost/posts"
  },
  "production": {
    "DATABASE_URI": "mysql://poor_user:poor_password@localhost/poor_posts"
  }
}
""")
        config = kaptan.Kaptan(handler='json')
        config.import_config(fobj.name)
        self.assertEqual(
            config.get('production.DATABASE_URI'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    @unittest.skipIf(yaml is None or not PY2, 'needs yaml')
    def test_yaml_safedump(self):
        testdict = {
            unicode("development"): {
                "DATABASE_URI": "mysql://root:123456@localhost/posts"
            },
            "production": {
                "DATABASE_URI": "mysql://poor_user:poor_password@localhost/poor_posts"
            }
        }

        config = kaptan.Kaptan()
        config.import_config(testdict)

        yamlconfig = kaptan.Kaptan()
        yamlconfig.import_config(config.get())

        self.assertIn('!!python/unicode', yamlconfig.export('yaml'))

        self.assertNotIn('!!python/unicode', yamlconfig.export('yaml', safe=True))

    @unittest.skipIf(yaml is None, 'needs yaml')
    def test_yaml_handler(self):
        config = kaptan.Kaptan(handler='yaml')
        config.import_config(yaml.dump(self.config))
        self.assertFalse(config.get("debug"))

    @unittest.skipIf(yaml is None, 'needs yaml')
    def test_yaml_file_handler(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml',
                                         delete=False) as fobj:
            fobj.write("""
development:
    DATABASE_URI: mysql://root:123456@localhost/posts

production:
    DATABASE_URI: mysql://poor_user:poor_password@localhost/poor_posts
""")
        config = kaptan.Kaptan(handler='yaml')
        config.import_config(fobj.name)
        self.assertEqual(
            config.get('production.DATABASE_URI'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    @unittest.skipIf(yaml is None, 'needs yaml')
    def test_yml_file_handler(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yml',
                                         delete=False) as fobj:
            fobj.write("""
development:
    DATABASE_URI: mysql://root:123456@localhost/posts

production:
    DATABASE_URI: mysql://poor_user:poor_password@localhost/poor_posts
""")
        config = kaptan.Kaptan()
        config.import_config(fobj.name)
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
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as fobj:
            fobj.write("""[development]
DATABASE_URI = mysql://root:123456@localhost/posts

[production]
DATABASE_URI = mysql://poor_user:poor_password@localhost/poor_posts
""")
        config = kaptan.Kaptan(handler='ini')
        config.import_config(fobj.name)
        self.assertEqual(
            config.get('production.database_uri'),
            'mysql://poor_user:poor_password@localhost/poor_posts'
        )

    def test_file_handler(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py',
                                         dir='.', delete=False) as fobj:
            fobj.write("""DATABASE = 'mysql://root:123456@localhost/girlz'
DEBUG = False
PAGINATION = {
    'per_page': 10,
    'limit': 20,
}
""")
        try:
            normalize_name = os.path.basename(fobj.name).rpartition('.')[0]
            config = kaptan.Kaptan(handler='file')
            config.import_config(normalize_name)
            self.assertEqual(config.get("PAGINATION.limit"), 20)
        finally:
            os.unlink(fobj.name)

    def test_invalid_key(self):
        config = kaptan.Kaptan()
        config.import_config(self.config)

        self.assertRaises(KeyError, config.get, 'invalidkey')
        self.assertRaises(KeyError, config.get, 'invaliddict.invalidkey')

    def test_invalid_key_with_default(self):
        config = kaptan.Kaptan()
        config.import_config(self.config)

        self.assertEqual(config.get('invalid_key', 'default_value'),
                         'default_value')
        self.assertEqual(config.get('invalid_key.bar.baz', 'default_value'),
                         'default_value')

    def test_default_value_none(self):
        config = kaptan.Kaptan()
        config.import_config(self.config)

        self.assertIsNone(config.get("invalid_key", None))
        self.assertIsNone(config.get("invalid_key.bar.baz", None))

    def test_get_all_config(self):
        config = kaptan.Kaptan()
        config.import_config(self.config)

        self.assertIsInstance(config.get(), dict)
        self.assertIsInstance(config.get(''), dict)

if __name__ == '__main__':
    unittest.main()
