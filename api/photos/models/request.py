from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Request(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    path = models.CharField(max_length=2048)
    method = models.CharField(max_length=10)
    ip_address = models.GenericIPAddressField(null=True)
    user_agent = models.TextField(blank=True)
    referer = models.URLField(max_length=2048, blank=True)
    status_code = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.status_code} {self.method} {self.path}'
