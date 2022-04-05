from rest_framework import serializers

from photos.models import Thumbnail


class ThumbnailSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='image')
    name = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_name(obj: Thumbnail):
        return obj.image.name

    class Meta:
        model = Thumbnail
        fields = (
            'url', 'name', 'type', 'width', 'height', 'is_watermarked',
        )
