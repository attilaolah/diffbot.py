# Python [Diffbot][1] API

[![Build Status](https://travis-ci.org/attilaolah/diffbot.py.png?branch=master)](https://travis-ci.org/attilaolah/diffbot.py)
[![Coverage Status](https://coveralls.io/repos/attilaolah/diffbot.py/badge.png)](https://coveralls.io/r/attilaolah/diffbot.py)
[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/attilaolah/diffbot.py/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

How to use it:

```python
>>> import diffbot
>>> json_result = diffbot.article('https://github.com', token='…')
```

The above simple example is a shortcut for using the `diffbot.Client` class.

```python
>>> import diffbot
>>> client = diffbot.Client(token='…')
>>> json_result = client.article('https://github.com')
```

The above calls are shortcuts for using the `diffbot.api()` function and the
`diffbot.Client.api` method:

```python
>>> import diffbot
>>> client = diffbot.Client(token='…')
>>> json_result = client.api('article', 'https://github.com')
```

You can test the module easily from the command line:

```sh
$ python diffbot.py -h
usage: diffbot.py [-h] [-a] api url token

positional arguments:
  api         API to call. One one of 'article', 'frontpage', 'product',
              'image' or 'classifier'.
  url         URL to pass as the 'url' parameter.
  token       API key (token). Get one at https://www.diffbot.com/.

optional arguments:
  -h, --help  show this help message and exit
  -a, --all   Request all fields.

$ python diffbot.py article https://github.com TOKEN
```

```json
{
  "icon": "https://github.com:443/apple-touch-icon-144.png",
    "sections": [
      …
  ],
  "title": "Build software better, together.",
  "url": "https://github.com/"
}
```

## Features:

* Python 3 support
* Google App Engine support
* [Requests][2] support (but no dependency)
* Simple & small (<100 LOC)
* [CI][3] + [100% test coverage][4]
* Passes `pyflakes`, `pep8`, `flake8`, `pylint` score 10/10


[1]: https://www.diffbot.com
[2]: http://docs.python-requests.org
[3]: https://travis-ci.org/attilaolah/diffbot.py
[4]: https://coveralls.io/r/attilaolah/diffbot.py
