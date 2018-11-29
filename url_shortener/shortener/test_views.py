from functools import partial
import json

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from .controller import create_shortened


class ShortenedUrlsAPITests(TestCase):

    API_URL = reverse('shortened_urls_api')

    def post(self, *args, **kwargs):
        json_post = partial(self.client.post, content_type='application/json')
        return json_post(*args, **kwargs)

    def test_create_shortened_url_valid(self):
        resp = self.post(
            self.API_URL,
            data=json.dumps({'url': 'https://www.google.com/'}),
        )
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertTrue(data['shortened_url'])

    def test_create_shortened_url_invalid_url(self):
        resp = self.post(
            self.API_URL,
            data=json.dumps({'url': 'aefoiheafioh'}),
        )
        self.assertEqual(resp.status_code, 400)

    def test_create_shortened_url_invalid_payload(self):
        resp = self.post(
            self.API_URL,
            data=json.dumps({'foo': 'bar'}),
        )
        self.assertEqual(resp.status_code, 400)


class RedirectShortenedTests(TestCase):

    def test_successful_redirect(self):
        expanded = 'https://www.google.com/'
        shortened = create_shortened(expanded)
        resp = self.client.get(shortened)
        self.assertEquals(resp.status_code, 301)
        self.assertEquals(resp.url, expanded)

    def test_unsuccessful_redirect(self):
        resp = self.client.get(settings.DOMAIN + 'superbogusurl')
        self.assertEquals(resp.status_code, 404)
