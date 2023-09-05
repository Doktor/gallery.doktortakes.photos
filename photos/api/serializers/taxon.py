from django.db.models import Q
from rest_framework import serializers

from photos.api.fields import TaxonCatalogIdField
from photos.models import Taxon, PhotoTaxon


class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = (
            "catalog_id", "parent_catalog_id", "passthrough_parent_catalog_id",
            "name", "slug", "rank", "common_name", "created_date", "updated_date"
        )


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
