from django.db import models


class License(models.Model):
    display_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=500, blank=True)
