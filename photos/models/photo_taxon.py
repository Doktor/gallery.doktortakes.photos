from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class PhotoTaxon(models.Model):
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)
    taxon = models.ForeignKey('Taxon', on_delete=models.CASCADE)

    rating = models.PositiveSmallIntegerField(default=0, validators=[
        MinValueValidator(0),
        MaxValueValidator(5),
    ])
    notes = models.TextField(blank=True)

    created_date = models.DateTimeField(auto_now_add=True, editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=False)
