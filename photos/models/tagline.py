from django.db import models


class Tagline(models.Model):
    text = models.CharField(max_length=500)

    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)
