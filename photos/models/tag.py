from django.db import models
from django.urls import reverse


class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100, blank=True)

    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Tag: #{self.slug}"

    def get_absolute_url(self) -> str:
        return reverse('tag', kwargs={'slug': self.slug})
