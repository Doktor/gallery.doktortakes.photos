from django.db import models
from django.urls import reverse


class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    def __str__(self):
        return f"Tag: #{self.slug}"
