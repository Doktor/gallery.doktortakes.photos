from rest_framework import serializers

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
