from django.urls import path

from . import views

urlpatterns = [
    path('', views.ShortenedUrlsAPI.as_view(), name='shortened_urls_api'),
]
