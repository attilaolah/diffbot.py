Python Diffbot_ API
===================

.. image:: https://d2weczhvl823v0.cloudfront.net/attilaolah/diffbot.py/trend.png
   :target: https://bitdeli.com/free
   :alt: Bitdeli
.. image:: https://travis-ci.org/attilaolah/diffbot.py.png?branch=master
   :target: https://travis-ci.org/attilaolah/diffbot.py
   :alt: Build Status
.. image:: https://coveralls.io/repos/attilaolah/diffbot.py/badge.png?branch=master
   :target: https://coveralls.io/r/attilaolah/diffbot.py
   :alt: Coverage Status

How to use it:
--------------

.. code:: python

    >>> import diffbot
    >>> json_result = diffbot.article('https://github.com', token='…')

The above simple example is a shortcut for using the ``diffbot.Client``
class.

.. code:: python

    >>> import diffbot
    >>> client = diffbot.Client(token='…')
    >>> json_result = client.article('https://github.com')

The above calls are shortcuts for using the ``diffbot.api()`` function
and the ``diffbot.Client.api`` method:

.. code:: python

    >>> import diffbot
    >>> client = diffbot.Client(token='…')
    >>> json_result = client.api('article', 'https://github.com')

To ``POST`` data (text or HTML) to the API, use the ``text`` or ``html``
arguments:

.. code:: python

    >>> import diffbot
    >>> client = diffbot.Client(token='…')
    >>> json_result = client.api('article', 'https://github.com', html='''
    ... <h1>Introducing GitHub Traffic Analytics</h1>
    ... <p>We want to kick off 2014 with a bang, so today we're happy to launch
    ... traffic analytics!</p>
    ... ''')

Command line interface:
-----------------------

.. code:: sh

    $ python diffbot.py -h
    usage: diffbot.py [-h] [-a] [-f FILE] api url token

    positional arguments:
      api                   API to call. One one of 'article', 'frontpage',
                            'product', 'image' or 'analyze'.
      url                   URL to pass as the 'url' parameter.
      token                 API key (token). Get one at https://www.diffbot.com/.

    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             Request all fields.
      -f FILE, --file FILE  File to read data from. Use '-' to read from STDIN.

    $ python diffbot.py article https://github.com TOKEN

Output of the above example:

.. code:: json

    {
      "icon": "https://github.com:443/apple-touch-icon-144.png",
      "sections": [
          …
      ],
      "title": "Build software better, together.",
      "url": "https://github.com/"
    }

Features:
---------

-  Python 2+3 support
-  Google App Engine support
-  Requests_ support (but no dependency)
-  Passes ``pyflakes``, ``pep8``, ``flake8``, ``pylint`` score 10/10
-  Simple & small (1 file, <200 LOC)
-  Command line interface

.. _Diffbot: https://www.diffbot.com
.. _Requests: http://docs.python-requests.org
.. _`100% test coverage`: https://coveralls.io/r/attilaolah/diffbot.py
