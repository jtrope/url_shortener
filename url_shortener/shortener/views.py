import json

from django.db import transaction
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect
from django.views import View

from .controller import (
    create_url_obj,
    get_expanded_url,
    get_shortened_url,
)
from .exceptions import ShortenerException


class ShortenedUrlsAPI(View):

    @transaction.atomic
    def post(self, request):
        data = json.loads(request.body)
        url = data.get('url')
        if not url:
            return JsonResponse({'error': 'Must provide url value'}, status=400)

        try:
            url_obj = create_url_obj(url)
            shortened_url = get_shortened_url(url_obj)
        except ShortenerException as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse(
            {'shortened_url': shortened_url},
            status=201
        )


def redirect_shortened(request, shortened_path):
    try:
        url = get_expanded_url(shortened_path)
    except ShortenerException:
        return HttpResponseNotFound('<h1>Uh-Oh, could not find a link!</h1>')

    return redirect(url, permanent=True)
