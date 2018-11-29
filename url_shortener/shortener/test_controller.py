import base64

from django.test import TestCase

from . import controller
from .models import Url


class ShortenerControllerTests(TestCase):

    def test_get_shortened_path(self):
        # Shortened path should return a base64 repr of the row's pk
        expanded = 'https://www.google.com/'
        url_obj = Url.objects.create(value=expanded)
        pk = str(url_obj.pk)
        expected = base64.urlsafe_b64encode(str.encode(pk)).decode('utf-8')
        self.assertEquals(expected, controller._get_shortened_path(url_obj))

    def test_create_shortened_url(self):
        expanded = 'https://www.google.com/'
        shortened_url = controller.create_shortened_url(expanded)

        # url should end with the shortened path
        url_obj = Url.objects.get(value=expanded)
        shortened_path = controller._get_shortened_path(url_obj)
        self.assertTrue(shortened_url.endswith(shortened_path))

        # Re-creating should not create a new DB entry
        controller.create_shortened_url('https://www.google.com/')
        self.assertEquals(Url.objects.count(), 1)

    def test_get_expanded_url(self):
        expanded = 'https://www.google.com/'
        url_obj = Url.objects.create(value=expanded)

        shortened_path = controller._get_shortened_path(url_obj)
        expanded = controller.get_expanded_url(shortened_path)
        self.assertEquals(expanded, url_obj.value)



