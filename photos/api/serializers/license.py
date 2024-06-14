from rest_framework import serializers

from photos.models import License


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = ('id', 'display_name', 'full_name', 'description', 'link')
