import base64
import binascii

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import URLValidator

from .exceptions import ShortenerException
from .models import Url

def _validate_url(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        raise ShortenerException('%s is an invalid URL' % url)


def create_shortened(url, domain=settings.DOMAIN):
    _validate_url(url)
    url_obj, _ = Url.objects.get_or_create(value=url)
    pk = str(url_obj.pk)
    encoded = base64.urlsafe_b64encode(str.encode(pk))
    return domain + encoded.decode('utf-8')


def get_expanded(shortened):
    try:
        decoded = base64.urlsafe_b64decode(shortened)
        pk = int(decoded)
    except (binascii.Error, ValueError):
        raise ShortenerException('%s is an invalid shortened chunk' % shortened)

    try:
        url = Url.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise ShortenerException('Could not find a link matching %s' % shortened)

    return url.value
