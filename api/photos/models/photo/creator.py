from django.db import models


class Creator(models.Model):
    name = models.CharField(max_length=200)
