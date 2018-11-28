from django.db import models


class Url(models.Model):
    value = models.CharField(max_length=200, unique=True)
