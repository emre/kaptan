## kaptan ##
[![Build Status](https://drone.io/github.com/emre/kaptan/status.png)](https://drone.io/github.com/emre/kaptan/latest) &nbsp; <img src= "https://pypip.in/v/kaptan/badge.png"> &nbsp; <img src="https://pypip.in/d/kaptan/badge.png">


configuration manager.

<img src="https://raw.github.com/emre/kaptan/master/sparrow.gif">


### installation ###

```
pip install kaptan
```
or if you like 90s:

```
easy_install kaptan
```

or add kaptan directory to the your path.

### usage ###
**supported handlers**

    - dict
    - json
    - yaml
    - .ini
    - python file
    
**default (dict) handler**
```python
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

#output: 20
```
**json handler**
```python
config = kaptan.Kaptan(handler="json")
config.import_config('{"everything": 42}')

print config.get("everything")
# output: 42
```

**yaml handler**
```python
config = kaptan.Kaptan()
config.import_config("""
product:
  price:
    value: 12.65
    currency_list:
      - TL
      - EURO
""")
print config.get("product.price.currency_list.0")
# output: TL
```

or you can get from directly from the filename:

```python
config.import_config("configuration.yaml")
```

**.ini handler**

config.ini
```
[development]
database_uri = mysql://root:123456@localhost/posts

[production]
database_uri = mysql://poor_user:poor_password@localhost/poor_posts
```

```python
config = kaptan.Kaptan(handler="ini")
config.import_config('config.ini')

print config.get("production.database_uri")
#output: mysql://poor_user:poor_password@localhost/poor_posts
```
**file handler**

config.py
```python
DATABASE = 'mysql://root:123456@localhost/posts'
DEBUG = False
PAGINATION = {
    'per_page': 10,
    'limit': 20,
}
```
```python
config = kaptan.Kaptan(handler="file")
config.import_config('config')

print config.get("DEBUG")
# output: False
```
## exporting configuration ##
```python
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

```

```python
print config.export("yaml")
```
**output**:
```
debug: false
environment: DEV
pagination: {limit: 20, per_page: 10}
redis_uri: redis://localhost:6379/0
```

```python
print config.export("json")
```

output unindented json. ``.export`` accepts kwargs which pass into [json.dumps](http://docs.python.org/2/library/json.html#json.dump).

```python
print config.export("json", indent=4)
```

**output**:
```
{
    "environment": "DEV",
    "debug": false,
    "pagination": {
        "per_page": 10,
        "limit": 20
    },
    "redis_uri": "redis://localhost:6379/0"
}
```

``config.export('yaml')`` also supports the [kwargs for pyyaml](http://pyyaml.org/wiki/PyYAMLDocumentation#Dumper).

## cli ##
exporting (defaults to json)
```
$ echo "environment: DEV" > config.yaml
$ kaptan config.yaml --export json > config.json
$ cat config.json
{"environment": "DEV"}
```
getting a value
```
$ kaptan config.yaml --key environment
DEV
```
specifying the handler
```
$ mv config.yaml config.settings
$ kaptan config.settings --export json
Traceback (most recent call last):
  ...
RuntimeError: Unable to determine handler
$ kaptan config.settings --handler yaml --export json
{"environment": "DEV"}
```
## running tests ##
```
$ py.test tests.py
======================================================================================================== test session starts ========================================================================================================
platform linux2 -- Python 2.7.3 -- pytest-2.3.5
collected 9 items 

tests.py .........

===================================================================================================== 9 passed in 0.06 seconds ======================================================================================================
```
