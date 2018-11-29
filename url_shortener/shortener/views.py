import json

from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect
from django.views import View

from .controller import create_shortened, get_expanded
from .exceptions import ShortenerException


class ShortenedUrlsAPI(View):

    def post(self, request):
        data = json.loads(request.body)
        url = data.get('url')
        if not url:
            return JsonResponse({'error': 'Must provide url value'}, status=400)

        try:
            shortened = create_shortened(url)
        except ShortenerException as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse(
            {'shortened_url': shortened},
            status=201
        )


def redirect_shortened(request, base64shortened):
    try:
        url = get_expanded(base64shortened)
    except ShortenerException:
        return HttpResponseNotFound('<h1>Uh-Oh, could not find a link!</h1>')

    return redirect(url, permanent=True)
