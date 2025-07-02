from django.db import models
from django.conf import settings


class Book(models.Model):
    title = models.CharField(max_length=200, blank=False)
    author = models.CharField(max_length=100, blank=False)

    objects = models.Manager()


class Review(models.Model):
    stars = models.IntegerField()
    comment = models.TextField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    objects = models.Manager()
