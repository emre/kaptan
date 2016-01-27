kaptan
======

|pypi| |docs| |build-status| |license| |bitdeli|

configuration parser.

installation
------------

.. code-block:: sh

    $ pip install kaptan

FreeBSD port
~~~~~~~~~~~~

`devel/py-kaptan`_ package.

- To install the port: ``cd /usr/ports/devel/py-kaptan/ && make install clean``
- To add the package: ``pkg install devel/py-kaptan``

.. _devel/py-kaptan: https://freshports.org/devel/py-kaptan/

usage
-----

**supported handlers**

- dict
- json
- yaml
- .ini
- python file

**default (dict) handler**

.. code-block:: python

    config = kaptan.Kaptan()
    config.import_config({
        'environment': 'DEV',
        'redis_uri': 'redis://localhost:6379/0',
        'debug': False,
        'pagination': {
            'per_page': 10,
            'limit': 20,
        }
    })

    print config.get("pagination.limit")

    # output: 20

**json handler**

.. code-block:: python

    config = kaptan.Kaptan(handler="json")
    config.import_config('{"everything": 42}')

    print config.get("everything")
    # output: 42

**yaml handler**

.. code-block:: python

    config = kaptan.Kaptan(handler="yaml")
    config.import_config("""
    product:
      price:
        value: 12.65
        currency_list:
          1. TL
          2. EURO
    """)
    print config.get("product.price.currency_list.0")
    # output: TL

or you can get from directly from the filename:

``config.import_config("configuration.yaml")``

**.ini handler**

config.ini

.. code-block:: ini

   [development]
   database_uri = mysql://root:123456@localhost/posts

   [production]
   database_uri = mysql://poor_user:poor_password@localhost/poor_posts

.. code-block:: python

    config = kaptan.Kaptan(handler="ini")
    config.import_config('config.ini')

    print config.get("production.database_uri")
    # output: mysql://poor_user:poor_password@localhost/poor_posts

**file handler**

config.py

.. code-block:: python

    DATABASE = 'mysql://root:123456@localhost/posts'
    DEBUG = False
    PAGINATION = {
        'per_page': 10,
        'limit': 20,
    }

.. code-block:: python

   config = kaptan.Kaptan(handler="file")
   config.import_config('config')

   print config.get("DEBUG")
   # output: False

exporting configuration
-----------------------

.. code-block:: python

    config = kaptan.Kaptan(handler="file")
    config.import_config({
        'environment': 'DEV',
        'redis_uri': 'redis://localhost:6379/0',
        'debug': False,
        'pagination': {
            'per_page': 10,
            'limit': 20,
        }
    })

    print config.export("yaml")

**output**:

.. code-block:: yaml

    debug: false
    environment: DEV
    pagination: {limit: 20, per_page: 10}
    redis_uri: redis://localhost:6379/0

``print config.export("json")``

outputs unindented json. ``.export`` accepts kwargs which pass into
`json.dumps`.

.. _json.dumps: http://docs.python.org/2/library/json.html#json.dump

.. code-block:: python

   print config.export("json", indent=4)

**output**:

.. code-block:: json

    {
        "environment": "DEV",
        "debug": false,
        "pagination": {
            "per_page": 10,
            "limit": 20
        },
        "redis_uri": "redis://localhost:6379/0"
    }

``config.export('yaml')`` also supports the `kwargs for pyyaml`_.

.. _kwargs for pyyaml: http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper

New in Version 0.5.7: ``config.export('yaml', safe=True)`` will use ``.safe_dump``.

cli
---

exporting (defaults to json)

.. code-block:: sh

    $ echo "environment: DEV" > config.yaml
    $ kaptan config.yaml --export json > config.json
    $ cat config.json
    {"environment": "DEV"}

getting a value

.. code-block:: sh

    $ kaptan config.yaml --key environment
    DEV

specifying the handler

.. code-block:: sh

    $ mv config.yaml config.settings
    $ kaptan config.settings:yaml --export json
    {"environment": "DEV"}

config from stdin

.. code-block:: sh

    $ echo '{"source": "stdin"}' | kaptan -
    {"source": "stdin"}
    $ echo 'source: stdin' | kaptan -:yaml
    {"source": "stdin"}

merging configs

.. code-block:: sh

   $ echo "environment: PROD" > config.settings
   $ echo '{"source": "stdin"}' | kaptan - config.json config.settings:yaml
   {"environment": "PROD", "source": "stdin"}

setting default handler

.. code-block:: sh

    $ echo "source: stdin" | kaptan --handler yaml - config.settings
    {"environment": "PROD", "source": "stdin"}

writing json with yaml

.. code-block:: sh

    $ kaptan -:yaml -e json
    <type yaml here>
    <Ctrl + D>
    <get json here>

running tests
-------------

With `py.test`:

.. code-block:: sh

    $ py.test tests.py

or just:

.. code-block:: sh

    $ python -m unittest discover -v

contributors
------------

- `Cenk Altı <http://github.com/cenkalti>`_
- `Wesley Bitter <http://github.com/Wessie>`_
- `Mark Steve <http://github.com/marksteve>`_
- `Tony Narlock <http://github.com/tony>`_
- `Berker Peksag <http://github.com/berkerpeksag>`_

.. |pypi| image:: https://img.shields.io/pypi/v/kaptan.svg
    :alt: Python Package
    :target: http://badge.fury.io/py/kaptan

.. |build-status| image:: https://img.shields.io/travis/emre/kaptan.svg
   :alt: Build Status
   :target: https://travis-ci.org/emre/kaptan

.. |license| image:: https://img.shields.io/github/license/emre/kaptan.svg
    :alt: License 

.. |docs| image:: https://readthedocs.org/projects/kaptan/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://readthedocs.org/projects/kaptan/

.. |bitdeli| image:: https://d2weczhvl823v0.cloudfront.net/emre/kaptan/trend.png
   :alt: bitdeli badge
   :target: https://bitdeli.com/free