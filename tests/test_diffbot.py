"""Diffbot API tests."""
import json
import os.path
import unittest
import sys

import mock

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


TOKEN = 'test'

GITHUB_COM = 'https://github.com'


def fake_requests_get(url, params=None):
    """A stub `requests.get()` implementation."""
    api = urlparse.urlparse(url)
    url = urlparse.urlparse(params['url'])
    resource = os.path.join('tests', 'resources', url.netloc,
                            api.path.strip('/') + '.json')
    with open(resource, 'rb') as src:
        return FakeResponse(json.loads(src.read().decode('utf-8')))


def fake_urllib2_urlopen(url):
    """A stub `urllib2.urlopen()` implementation."""
    api = urlparse.urlparse(url)
    url = urlparse.urlparse(urlparse.parse_qs(api.query)['url'][0])
    resource = os.path.join('tests', 'resources', url.netloc,
                            api.path.strip('/') + '.json')
    return open(resource, 'rb')


class FakeResponse(object):
    """A stub `requests.Response` implementation."""

    def __init__(self, json_data):
        """Set up the json data."""
        self._json = json_data

    def json(self):
        """Return the JSON data."""
        return self._json


class ImportHook(object):
    """PEP-302-style import hook."""

    def __init__(self, *blocked_modules):
        """Block specific modules."""
        self._blocked_modules = blocked_modules
        for module in blocked_modules:
            for item in sys.modules.keys()[:]:
                if item.split('.')[0] == module:
                    del sys.modules[item]

    def find_module(self, fullname, path=None):
        """Find a specific module."""
        if fullname in self._blocked_modules:
            raise ImportError(fullname)


class ClientTest(unittest.TestCase):
    """API method tests."""

    def setUp(self):
        """Set up a mock patcher."""
        self.patcher = mock.patch('requests.get', fake_requests_get)
        self.patcher.start()
        import diffbot
        self.module = diffbot
        self.client = diffbot.Client(token=TOKEN)
        self.client_v1 = diffbot.Client(token=TOKEN, version=1)
        self.client_v2 = diffbot.Client(token=TOKEN, version=2)

    def tearDown(self):
        """Stop the patcher."""
        self.patcher.stop()

    def test_article(self):
        """Test the Article API."""
        result = self.module.article(GITHUB_COM, token=TOKEN)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_client_article(self):
        """Test the Article API."""
        result = self.client.article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')

    def test_client_article_v1(self):
        """Test the Article API version 1."""
        result = self.client_v1.article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')

    def test_client_article_v2(self):
        """Test the Article API version 2."""
        result = self.client_v2.article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')

    def test_article_fields(self):
        """Test the Article API with strings provided as a list."""
        result = self.module.article(GITHUB_COM, token=TOKEN, fields=[
            'url', 'type', 'title'])
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_article_fields_str(self):
        """Test the Article API with fields provided as a string."""
        result = self.module.article(GITHUB_COM, token=TOKEN, fields='*')
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_article_timeout(self):
        """Test the Article API with a timeout."""
        result = self.module.article(GITHUB_COM, token=TOKEN, timeout=10)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_frontpage(self):
        """Test the Frontpage API."""
        result = self.module.frontpage(GITHUB_COM, token=TOKEN)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_client_frontpage(self):
        """Test the Frontpage API."""
        result = self.client.frontpage(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_product(self):
        """Test the Product API."""
        result = self.module.product(GITHUB_COM, token=TOKEN)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'product')

    def test_client_product(self):
        """Test the Product API."""
        result = self.client.product(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'product')

    def test_image(self):
        """Test the Image API."""
        result = self.module.image(GITHUB_COM, token=TOKEN)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'image')

    def test_client_image(self):
        """Test the Image API."""
        result = self.client.image(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'image')

    def test_analyze(self):
        """Test the Classifier API."""
        result = self.module.analyze(GITHUB_COM, token=TOKEN)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_client_analyze(self):
        """Test the Classifier API."""
        result = self.client.analyze(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['type'], 'article')
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_invalid_api(self):
        """Test calling an invalid API.

        This should not make a request to the Diffbot API endpoint.
        """
        def raises():
            self.module.api('foo', GITHUB_COM, token=TOKEN)
        self.assertRaises(ValueError, raises)

    def test_invalid_api_client(self):
        """Test calling an invalid API using the Client object."""
        def raises():
            self.client.api('foo', GITHUB_COM)
        self.assertRaises(ValueError, raises)



class ClientTestUrllib(unittest.TestCase):
    """API method tests using urllib2 and urllib.

    This tests the scenario when the requests library is not installed."""

    def setUp(self):
        """Set up a mock patcher.

        This will make the `requests` library unavailable in `diffbot`.
        """
        self.patcher = mock.patch('urllib2.urlopen', fake_urllib2_urlopen)
        self.import_hook = ImportHook('requests')
        sys.meta_path.append(self.import_hook)
        self.patcher.start()
        import diffbot
        diffbot = reload(diffbot)
        del diffbot.requests
        self.module = diffbot
        self.client = diffbot.Client(token=TOKEN)

    def tearDown(self):
        """Stop the patcher."""
        self.patcher.stop()
        sys.meta_path.remove(self.import_hook)

    def test_article_client(self):
        """Test the Article API."""
        result = self.module.Client(TOKEN).article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')


class CmdLineTest(unittest.TestCase):
    """Test the command line interface."""

    def setUp(self):
        """Set up a mock patcher."""
        import sys
        self.patcher = mock.patch('requests.get', fake_requests_get)
        self.patcher.start()
        import diffbot
        self.module = reload(diffbot)
        self._sys_argv = sys.argv[:]
        sys.argv[:] = [self._sys_argv[0], 'image', GITHUB_COM, 'secret', '--all']

    def tearDown(self):
        """Stop the patcher."""
        import sys
        self.patcher.stop()
        sys.argv[:] = self._sys_argv[:]

    def test_article(self):
        """Test the Article API."""
        self.module._main()
