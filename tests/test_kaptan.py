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
import os.path
import sys
import tempfile

import pytest

import kaptan

try:
    import yaml
except ImportError:
    yaml = None


# python 2/3 compat
try:
    unicode = unicode
except NameError:
    # py changes unicode => str
    unicode = str

PY2 = sys.version_info[0] == 2


sentinel = object()


@pytest.fixture
def testconfig():
    return {
        'debug': False,
    }


def test_configuration_data(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    assert 'debug' in config.configuration_data


def test_main_get():
    config = kaptan.Kaptan()
    config.import_config({
        'show_comments': True,
        'entry_count': 10,
    })

    assert config.get("entry_count", 25) == 10
    assert config.get("entry_count") == 10
    assert config.get("show_comments", None)
    assert config.get("show_comments", False)


def test_nested_configuration():
    config = kaptan.Kaptan()
    config.import_config({
        'pagination': {
            'per_page': 20,
            'limit': 5,
        }
    })

    assert config.get("pagination.limit") == 5


def test_lists_on_configuration():
    config = kaptan.Kaptan()
    config.import_config({
        'servers': ['redis1', 'redis2', 'redis3'],
    })

    assert config.get('servers.0') == 'redis1'


def test_upsert(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    assert not config.get('debug')

    config.upsert('debug', True)
    assert config.get('debug')


def test_default_dict_handler(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    assert not config.configuration_data['debug']


def test_json_handler(testconfig):
    config = kaptan.Kaptan(handler='json')
    config.import_config(json.dumps(testconfig))

    assert not config.get('debug')


def test_json_file_handler(tmpdir):
    json_file = tmpdir.join('config.json')
    json_file.write("""{"development": {
"DATABASE_URI": "mysql://root:123456@localhost/posts"
},
"production": {
"DATABASE_URI": "mysql://poor_user:poor_password@localhost/poor_posts"
}
}
""")
    config = kaptan.Kaptan(handler='json')
    config.import_config(str(json_file))
    assert config.get(
        'production.DATABASE_URI'
    ) == 'mysql://poor_user:poor_password@localhost/poor_posts'


@pytest.mark.skipif(yaml is None or not PY2, reason='needs yaml')
def test_yaml_safedump(testconfig):
    testdict = {
        unicode("development"): {
            "DATABASE_URI": "mysql://root:123456@localhost/posts"
        },
        "production": {
            "DATABASE_URI": "mysql://poor_user:poor_password@localhost/poor_posts"  # NOQA
        }
    }

    config = kaptan.Kaptan()
    config.import_config(testdict)

    yamlconfig = kaptan.Kaptan()
    yamlconfig.import_config(config.get())

    assert '!!python/unicode' not in yamlconfig.export('yaml')
    assert '!!python/unicode' not in yamlconfig.export('yaml', safe=True)
    assert '!!python/unicode' in yamlconfig.export('yaml', safe=False)


@pytest.mark.skipif(yaml is None, reason='needs yaml')
def test_yaml_handler(testconfig):
    config = kaptan.Kaptan(handler='yaml')
    config.import_config(yaml.safe_dump(testconfig))
    assert not config.get("debug")


@pytest.mark.skipif(yaml is None, reason='needs yaml')
def test_yaml_file_handler(tmpdir, testconfig):
    yaml_file = tmpdir.join('config.yaml')

    yaml_file.write("""
development:
  DATABASE_URI: mysql://root:123456@localhost/posts

production:
  DATABASE_URI: mysql://poor_user:poor_password@localhost/poor_posts
""")
    config = kaptan.Kaptan(handler='yaml')
    config.import_config(str(yaml_file))
    assert config.get('production.DATABASE_URI') == \
        'mysql://poor_user:poor_password@localhost/poor_posts'


@pytest.mark.skipif(yaml is None, reason='needs yaml')
def test_yml_file_handler(tmpdir):
    yml_file = tmpdir.join('config.yml')
    yml_file.write("""
development:
  DATABASE_URI: mysql://root:123456@localhost/posts

production:
  DATABASE_URI: mysql://poor_user:poor_password@localhost/poor_posts
""")
    config = kaptan.Kaptan()
    config.import_config(str(yml_file))
    assert config.get('production.DATABASE_URI') == \
        'mysql://poor_user:poor_password@localhost/poor_posts'


def test_ini_handler(testconfig):
    value = """[development]
DATABASE_URI = mysql://root:123456@localhost/posts

[production]
DATABASE_URI = mysql://poor_user:poor_password@localhost/poor_posts
"""

    config = kaptan.Kaptan(handler='ini')
    config.import_config(value)

    assert config.get(
        'production.database_uri'
    ) == 'mysql://poor_user:poor_password@localhost/poor_posts'


def test_ini_file_handler(tmpdir, testconfig):
    ini_file = tmpdir.join('config.ini')
    ini_file.write("""[development]
DATABASE_URI = mysql://root:123456@localhost/posts

[production]
DATABASE_URI = mysql://poor_user:poor_password@localhost/poor_posts
""")
    config = kaptan.Kaptan(handler='ini')
    config.import_config(str(ini_file))
    assert config.get(
        'production.database_uri'
    ) == 'mysql://poor_user:poor_password@localhost/poor_posts'


def test_ini_file_dump(tmpdir):
    testdict = {
        "development": {
            "DATABASE_URI": "mysql://root:123456@localhost/posts"
        },
        "production": {
            "DATABASE_URI": "mysql://poor_user:poor_password@localhost/poor_posts"  # NOQA
        }
    }

    config = kaptan.Kaptan()
    config.import_config(testdict)

    ini_file = tmpdir.join('config.ini')
    config.export('ini', file_=str(ini_file))

    ini_config = kaptan.Kaptan(handler='ini')
    ini_config.import_config(str(ini_file))

    assert ini_config.get(
        'production.database_uri'
    ) == 'mysql://poor_user:poor_password@localhost/poor_posts'


def test_py_file_handler(testconfig, tmpdir, monkeypatch):
    py_file = tmpdir.join('config.py')
    py_file.write("""DATABASE = 'mysql://root:123456@localhost/girlz'
DEBUG = False
PAGINATION = {
'per_page': 10,
'limit': 20,
}
""")
    monkeypatch.syspath_prepend(str(tmpdir))
    normalize_name = str(py_file).rpartition('.')[0]
    config = kaptan.Kaptan(handler='file')
    config.import_config(normalize_name)
    assert config.get("PAGINATION.limit") == 20


def test_py_file_away_handler(tmpdir, testconfig):
    py_file = tmpdir.join('config2.py')
    py_file.write("""DATABASE = 'mysql://root:123456@localhost/girlz'
DEBUG = False
PAGINATION = {
'per_page': 10,
'limit': 20,
}
""")
    config = kaptan.Kaptan()
    config.import_config(str(py_file))
    assert config.get("PAGINATION.limit") == 20


def test_py_file_away_noexist_raises(tmpdir, testconfig):
    py_file = tmpdir.join('config3.py')

    config = kaptan.Kaptan()
    with pytest.raises(IOError):
        config.import_config(str(py_file))


def test_invalid_key(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    with pytest.raises(KeyError):
        config.get('invalidkey')
    with pytest.raises(KeyError):
        config.get('invaliddict.invalidkey')


def test_invalid_key_with_default(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    assert config.get('invalid_key', 'default_value') == 'default_value'
    assert config.get('invalid_key.bar.baz',
                      'default_value') == 'default_value'


def test_default_value_none(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    assert config.get("invalid_key", None) is None
    assert config.get("invalid_key.bar.baz", None) is None


def test_get_all_config(testconfig):
    config = kaptan.Kaptan()
    config.import_config(testconfig)

    assert isinstance(config.get(), dict)
    assert isinstance(config.get(''), dict)
