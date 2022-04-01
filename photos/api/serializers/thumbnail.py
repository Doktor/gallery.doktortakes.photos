from rest_framework import serializers

from photos.models import Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='image')

    class Meta:
        model = Thumbnail
        fields = (
            'url', 'type', 'width', 'height',
        )
