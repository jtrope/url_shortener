import base64

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import URLValidator

from .exceptions import ShortenerException
from .models import Url


def create_url_obj(url):
    _validate_url(url)

    url_obj, created = Url.objects.get_or_create(expanded=url)
    if created:
        url_obj.shortened = _generate_shortened_path(url_obj)
        url_obj.save()

    return url_obj


def get_shortened_url(url_obj, domain=settings.DOMAIN):
    return domain + url_obj.shortened


def get_expanded_url(shortened_path):
    try:
        url_obj = Url.objects.get(shortened=shortened_path)
    except ObjectDoesNotExist:
        raise ShortenerException('Could not find a link matching %s' % shortened_path)

    return url_obj.expanded


def _generate_shortened_path(url_obj):
    as_str = str(url_obj.pk)
    encoded = base64.urlsafe_b64encode(str.encode(as_str))
    return encoded.decode('utf-8') # Return as str


def _validate_url(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        raise ShortenerException('%s is an invalid URL' % url)
