"""Diffbot API Wrapper."""
import json
import urllib
import urllib2

try:
    import requests
except ImportError:
    pass


ENCODING = 'utf-8'

API_ROOT = 'http://api.diffbot.com'
API_VERSION = 2


class Client(object):
    """Diffbot client."""

    _apis = frozenset(('article', 'frontpage', 'product', 'image', 'analyze'))

    def __init__(self, token, version=API_VERSION):
        """Initialise the client."""
        self._token = token
        self._version = version

    @staticmethod
    def _get(url, params=None):
        """HTTP GET request."""
        try:
            return requests.get(url, params=params).json()
        except NameError:
            url = '{0}?{1}'.format(url, urllib.urlencode(params))
            return json.loads(urllib2.urlopen(url).read().decode(ENCODING))

    @staticmethod
    def _post(url, data, content_type, params=None):
        """HTTP POST request."""
        try:
            return requests.post(url, params=params, data=data, headers={
                'Content-Type': content_type,
            }).json()
        except NameError:
            url = '{0}?{1}'.format(url, urllib.urlencode(params))
            req = urllib2.Request(url, data.encode(ENCODING), {
                'Content-Type': content_type,
            })
            return json.loads(urllib2.urlopen(req).read().decode(ENCODING))

    def api(self, name, url, **kwargs):
        """Generic API method."""
        if name not in self._apis:
            raise ValueError('API name must be one of {0}, not {1!r}.'.format(
                tuple(self._apis), name))
        fields = kwargs.get('fields')
        timeout = kwargs.get('timeout')
        content_type = kwargs.get('content_type', 'text/plain')
        text = kwargs.get('text')
        params = {'url': url, 'token': self._token}
        if timeout:
            params['timeout'] = timeout
        if fields:
            if not isinstance(fields, str):
                fields = ','.join(sorted(fields))
            params['fields'] = fields
        url = '{0}/v{1}/{2}'.format(API_ROOT, self._version, name)
        if text:
            return self._post(url, text, content_type, params=params)
        return self._get(url, params=params)

    def article(self, url, **kwargs):
        """Article API."""
        return self.api('article', url, **kwargs)

    def frontpage(self, url, **kwargs):
        """Frontpage API."""
        return self.api('frontpage', url, **kwargs)

    def product(self, url, **kwargs):
        """Product API."""
        return self.api('product', url, **kwargs)

    def image(self, url, **kwargs):
        """Image API."""
        return self.api('image', url, **kwargs)

    def analyze(self, url, **kwargs):
        """Classifier (analyze) API."""
        return self.api('analyze', url, **kwargs)


def api(name, url, token, **kwargs):
    """Shortcut for caling methods on `Client(token, version)`."""
    return Client(token).api(name, url, **kwargs)


def article(url, token, **kwargs):
    """Shortcut for `Client(token, version).article(url)`."""
    return api('article', url, token, **kwargs)


def frontpage(url, token, **kwargs):
    """Shortcut for `Client(token, version).frontpage(url)`."""
    return api('frontpage', url, token, **kwargs)


def product(url, token, **kwargs):
    """Shortcut for `Client(token, version).product(url)`."""
    return api('product', url, token, **kwargs)


def image(url, token, **kwargs):
    """Shortcut for `Client(token, version).image(url)`."""
    return api('image', url, token, **kwargs)


def analyze(url, token, **kwargs):
    """Shortcut for `Client(token, version).analyze(url)`."""
    return api('analyze', url, token, **kwargs)


def _main():
    """Command line tool."""
    import argparse
    import sys
    parser = argparse.ArgumentParser()
    parser.add_argument("api", help="""
        API to call.
        One one of 'article', 'frontpage', 'product', 'image' or 'analyze'.
    """)
    parser.add_argument("url", help="""
        URL to pass as the 'url' parameter.
    """)
    parser.add_argument('token', help="""
        API key (token).
        Get one at https://www.diffbot.com/.
    """)
    parser.add_argument('-a', '--all', help="""
        Request all fields.
    """, action='store_true')
    parser.add_argument('-f', '--file', help="""
        File to read data from.
        Use '-' to read from STDIN.
    """)
    fields = text = None
    _args = parser.parse_args()
    if _args.all:
        fields = '*'
    if _args.file == '-':
        text = sys.stdin.read()
    elif _args.file:
        with open(_args.file, 'rb') as src:
            text = src.read().decode(ENCODING)
    print(json.dumps((api(_args.api, _args.url, _args.token,
                          text=text or None,
                          fields=fields)),
                     sort_keys=True,
                     indent=2))


if __name__ == '__main__':
    _main()  # pragma: no cover
