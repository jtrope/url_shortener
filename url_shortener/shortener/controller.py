import base64
import binascii

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import URLValidator

from .exceptions import ShortenerException
from .models import Url


def create_shortened_url(url, domain=settings.DOMAIN):
    _validate_url(url)
    url_obj, _ = Url.objects.get_or_create(value=url)
    path = _get_shortened_path(url_obj)
    return domain + path


def get_expanded_url(shortened_path):
    try:
        decoded = base64.urlsafe_b64decode(shortened_path)
        pk = int(decoded)
    except (binascii.Error, ValueError):
        raise ShortenerException('%s is an invalid shortened path' % shortened_path)

    try:
        url_obj = Url.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise ShortenerException('Could not find a link matching %s' % shortened_path)

    return url_obj.value


def _get_shortened_path(url_obj):
    as_str = str(url_obj.pk)
    encoded = base64.urlsafe_b64encode(str.encode(as_str))
    return encoded.decode('utf-8') # Return as str


def _validate_url(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        raise ShortenerException('%s is an invalid URL' % url)
