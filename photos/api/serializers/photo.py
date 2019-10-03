from django.urls import reverse

from rest_framework import serializers

from photos.models import Photo

from collections import OrderedDict


class PhotoSerializer(serializers.ModelSerializer):
    # Image links
    image = serializers.ImageField(use_url=True, read_only=True)
    square_thumbnail = serializers.ImageField(use_url=True, read_only=True)
    thumbnail = serializers.ImageField(use_url=True, read_only=True, allow_null=True)

    # Links
    url = serializers.CharField(read_only=True, source='get_absolute_url')
    download = serializers.CharField(read_only=True, source='get_download_url')
    admin = serializers.SerializerMethodField(read_only=True, allow_null=True)

    # Metadata
    taken = serializers.DateTimeField(
        read_only=True, format="%A, %Y-%m-%d, %-I:%M:%S %p")
    index = serializers.IntegerField(
        read_only=True, allow_null=True, default=None)
    exif = serializers.DictField(read_only=True, source='get_exif')

    def get_admin(self, obj: Photo):
        if self.context.get('is_staff', False):
            return reverse('admin:photos_photo_change', args=[obj.pk])
        else:
            return None

    def to_representation(self, instance: Photo) -> dict:
        instance.index = self.context.get('index', None)

        result = super().to_representation(instance)

        # Don't serialize null values
        return OrderedDict(
            [(key, result[key]) for key in result if result[key] is not None])

    class Meta:
        model = Photo
        fields = (
            'image', 'square_thumbnail', 'thumbnail',
            'url', 'download', 'admin',
            'taken',
            'width', 'height', 'md5', 'index',
            'path', 'exif',
        )


class SimplePhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    square_thumbnail = serializers.ImageField(use_url=True)
    url = serializers.CharField(read_only=True, source='get_absolute_url')

    class Meta:
        model = Photo
        fields = ('image', 'square_thumbnail', 'url')


class PhotoThumbnailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(use_url=True)

    class Meta:
        model = Photo
        fields = ('thumbnail',)
