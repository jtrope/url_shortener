from django.db import models


class Url(models.Model):
    expanded = models.CharField(max_length=200, unique=True)
    shortened = models.CharField(max_length=50, unique=True)
