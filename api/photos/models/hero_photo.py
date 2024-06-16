from django.db import models


class HeroPhoto(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=500, blank=True)
    x_position = models.CharField(max_length=20, default='center')

    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)
