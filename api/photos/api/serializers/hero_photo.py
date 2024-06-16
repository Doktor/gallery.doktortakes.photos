from rest_framework import serializers

from photos.models import HeroPhoto


class HeroPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroPhoto
        fields = (
            'image', 'title', 'description', 'x_position',
        )