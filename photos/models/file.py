from django.db import models


def get_file_path(file: 'File', filename: str) -> str:
    return f"files/{file.name}"


class File(models.Model):
    file = models.FileField(upload_to=get_file_path, blank=True, null=True)

    name = models.CharField(max_length=100)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)
