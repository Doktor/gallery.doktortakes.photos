from django.db.models import Q
from rest_framework import serializers

from photos.api.fields import TaxonCatalogIdField
from photos.models import PhotoTaxon


class PhotoTaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoTaxon
        fields = (
            "rating", "notes",
        )


class ManagePhotoTaxonSerializer(serializers.ModelSerializer):
    taxon = TaxonCatalogIdField(queryset=Q())

    class Meta:
        model = PhotoTaxon
        fields = (
            "taxon", "rating", "notes",
        )
