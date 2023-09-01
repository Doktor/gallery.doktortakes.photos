from rest_framework import serializers

from photos.models import Taxon


class TaxonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taxon
        fields = ("catalog_id", "name", "slug", "rank", "common_name", "created_date", "updated_date")
