"""Diffbot API tests."""
import json
import os.path
import unittest
import urlparse

import mock

import diffbot


TOKEN = 'test'

GITHUB_COM = 'https://github.com'


def fake_requests_get(url, params=None):
    """A stub requests.get() implementation."""
    api = urlparse.urlparse(url)
    url = urlparse.urlparse(params['url'])
    resource = os.path.join('tests', 'resources', url.netloc,
                            api.path.strip('/') + '.json')
    with open(resource, 'rb') as src:
        return FakeResponse(json.load(src))


class FakeResponse(object):
    """A stub `requests.Response` implementation."""

    def __init__(self, json_data):
        """Set up the json data."""
        self._json = json_data

    def json(self):
        """Return the JSON data."""
        return self._json


class ArticleTest(unittest.TestCase):
    """Article API tests."""

    def setUp(self):
        """Set up a mock patcher."""
        self.patcher = mock.patch('requests.get', fake_requests_get)
        self.patcher.start()
        self.client = diffbot.Client(token=TOKEN)
        self.client_v1 = diffbot.Client(token=TOKEN, version=1)
        self.client_v2 = diffbot.Client(token=TOKEN, version=2)

    def tearDown(self):
        """Stop the patcher."""
        self.patcher.stop()

    def test_article(self):
        """Test the Article API."""
        result = diffbot.article(GITHUB_COM, token=TOKEN)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_client_article(self):
        """Test the Article API."""
        result = self.client.article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_client_article_v1(self):
        """Test the Article API."""
        result = self.client_v1.article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')

    def test_client_article_v2(self):
        """Test the Article API."""
        result = self.client_v2.article(GITHUB_COM)
        self.assertEqual(result['url'], GITHUB_COM)
        self.assertEqual(result['title'], 'Build software better, together.')
