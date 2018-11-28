from django.views import View

from django.http import JsonResponse

class ShortenedUrlsAPI(View):

    def get(self, request):
        return JsonResponse({'hello': 'world'})
