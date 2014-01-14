"""Diffbot API Wrapper."""
import json

try:
    import requests
except ImportError:
    import urllib
    import urllib2


API_ROOT = 'http://api.diffbot.com/'
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
            if params is not None:
                url = '{0}?{1}'.format(url, urllib.urlencode(params))
            return json.load(urllib2.urlopen(url))

    def api(self, name, url, fields=None, timeout=None):
        """Generic API method."""
        if name not in self._apis:
            raise ValueError('API name must be one of {0}, not {1!r}.'.format(
                tuple(self._apis), name))
        params = {'url': url, 'token': self._token}
        if timeout is not None:
            params['timeout'] = timeout
        if fields is not None:
            if not isinstance(fields, str):
                fields = ','.join(sorted(fields))
            params['fields'] = fields
        url = '{0}/v{1}/{2}'.format(API_ROOT, self._version, name)
        return self._get(url, params=params)

    def article(self, url, fields=None, timeout=None):
        """Article API."""
        return self.api('article', url, fields=fields, timeout=timeout)

    def frontpage(self, url, timeout=None):
        """Frontpage API."""
        return self.api('frontpage', url, timeout=timeout)

    def product(self, url, fields=None, timeout=None):
        """Product API."""
        return self.api('product', url, fields=fields, timeout=timeout)

    def image(self, url, fields=None, timeout=None):
        """Image API."""
        return self.api('image', url, fields=fields, timeout=timeout)

    def analyze(self, url, fields=None, timeout=None):
        """Classifier (analyze) API."""
        return self.api('analyze', url, fields=fields, timeout=timeout)


def api(name, url, token, fields=None, timeout=None):
    """Shortcut for caling methods on `Client(token, version)`."""
    return Client(token).api(name, url, fields, timeout)


def article(url, token, fields=None, timeout=None):
    """Shortcut for `Client(token, version).article(url)`."""
    return api('article', url, token, fields, timeout)


def frontpage(url, token, timeout=None):
    """Shortcut for `Client(token, version).frontpage(url)`."""
    return api('frontpage', url, token, timeout)


def product(url, token, fields=None, timeout=None):
    """Shortcut for `Client(token, version).product(url)`."""
    return api('product', url, token, fields, timeout)


def image(url, token, fields=None, timeout=None):
    """Shortcut for `Client(token, version).image(url)`."""
    return api('image', url, token, fields, timeout)


def analyze(url, token, fields=None, timeout=None):
    """Shortcut for `Client(token, version).analyze(url)`."""
    return api('analyze', url, token, fields, timeout)


def _main():
    """Command line tool."""
    import argparse
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
    _args = parser.parse_args()
    fields = None
    if _args.all:
        fields = '*'
    print(json.dumps((api(_args.api, _args.url, _args.token,
                          fields=fields)),
                     sort_keys=True,
                     indent=2))


if __name__ == '__main__':
    _main()  # pragma: no cover
