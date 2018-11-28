import binascii
import base64
import json

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import redirect

from .models import Url


# TODO: Remove: Insecure!
@method_decorator(csrf_exempt, name='dispatch')
class ShortenedUrlsAPI(View):

    def post(self, request):
        # TODO: Move business logic out of view
        data = json.loads(request.body)
        try:
            url_val = data['url']
        except KeyError:
            return JsonResponse({'error': 'Must provide url value'}, status=400)

        validator = URLValidator()
        try:
            validator(url_val)
        except ValidationError:
            return JsonResponse({'error': 'Invalid URL'}, status=400)

        url, _ = Url.objects.get_or_create(value=url_val)
        pk = str(url.pk)
        encoded = base64.urlsafe_b64encode(str.encode(pk))
        return JsonResponse(
            {'shortened_url': settings.DOMAIN + encoded.decode('utf-8')}
        )


def redirect_shortened(request, base64shortened):
    try:
        decoded = base64.urlsafe_b64decode(base64shortened)
        pk = int(decoded)
    except (binascii.Error, ValueError):
        # TODO: Handle error
        raise

    try:
        url = Url.objects.get(pk=pk)
    except ObjectDoesNotExist:
        # TODO: Handle error
        raise

    return redirect(url.value, permanent=True)
