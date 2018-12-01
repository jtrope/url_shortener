import base64

from django.test import TestCase

from .. import controller
from ..models import Url


class ShortenerControllerTests(TestCase):

    def test_generate_shortened_path(self):
        # Shortened path should return a base64 repr of the row's pk
        expanded = 'https://www.google.com/'
        url_obj = Url.objects.create(expanded=expanded, shortened='foobar')
        pk = str(url_obj.pk)
        expected = base64.urlsafe_b64encode(str.encode(pk)).decode('utf-8')
        self.assertEquals(expected, controller._generate_shortened_path(url_obj))

    def test_create_url_obj(self):
        expanded = 'https://www.google.com/'
        url_obj = controller.create_url_obj(expanded)

        shortened_path = controller._generate_shortened_path(url_obj)
        self.assertEqual(url_obj.expanded, expanded)
        self.assertEqual(url_obj.shortened, shortened_path)

        # Re-creating should not create a new DB entry
        controller.create_url_obj(expanded)
        self.assertEquals(Url.objects.count(), 1)

    def test_get_shortened_url(self):
        url_obj = controller.create_url_obj('https://www.google.com/')
        domain = 'https://www.trope.ly/'
        shortened_url = controller.get_shortened_url(
            url_obj,
            domain=domain
        )
        self.assertEquals(
            shortened_url,
            domain + url_obj.shortened,
        )

    def test_get_expanded_url(self):
        expanded = 'https://www.google.com/'
        url_obj = controller.create_url_obj(expanded)

        expanded = controller.get_expanded_url(url_obj.shortened)
        self.assertEquals(expanded, expanded)
