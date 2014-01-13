"""Diffbot API Wrapper."""
import json
import urllib
import urllib2

import requests


API_ROOT = 'http://api.diffbot.com'
API_VERSION = 2


class Client(object):
    """Diffbot client."""

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
                url = '{}?{}'.format(url, urllib.urlencode(params))
            return json.load(urllib2.urlopen(url))

    def api(self, name, params=None):
        """Generic API method."""
        params = params or {}
        params.setdefault('token', self._token)
        url = '{}/v{}/{}'.format(API_ROOT, self._version, name)
        return self._get(url, params=params)

    def __fields_api(name, supports_fields=True):
        """Generate an API that supports the 'fields' parameter."""
        def _api_method(self, url, fields=None, timeout=None):
            """Auto-generated API method."""
            params = {'url': url}
            if timeout is not None:
                params['timeout'] = timeout
            if supports_fields and fields is not None:
                params['fields'] = fields
            return self.api(name, params=params)
        return _api_method

    article = __fields_api('article')
    frontpage = __fields_api('frontpage', False)
    product = __fields_api('product')
    image = __fields_api('image')
    classifier = __fields_api('analyze')


def api(name, url, token, fields=None, timeout=None):
    """Shortcut for caling methods on Client(token, version)."""
    return getattr(Client(token), name)(url, fields, timeout)


def article(url, token=None, fields=None, timeout=None):
    """Shortcut for `Client(token, version).article(url)`."""
    return api('article', url, token, fields, timeout)


def frontpage(url, token=None, timeout=None):
    """Shortcut for `Client(token, version).frontpage(url)`."""
    return api('frontpage', url, token, timeout)


def product(url, token=None, fields=None, timeout=None):
    """Shortcut for `Client(token, version).product(url)`."""
    return api('product', url, token, fields, timeout)


def image(url, token=None, fields=None, timeout=None):
    """Shortcut for `Client(token, version).image(url)`."""
    return api('image', url, token, fields, timeout)


def _main():
    """Command line tool."""
    import argparse
    import pprint
    parser = argparse.ArgumentParser()
    parser.add_argument("api", help="API to call")
    parser.add_argument("url", help="URL to pass as the 'url' parameter")
    parser.add_argument('token', help='API key (token)')
    _args = parser.parse_args()
    pprint.pprint(api(_args.api, _args.url, token=_args.token))


if __name__ == '__main__':
    _main()
