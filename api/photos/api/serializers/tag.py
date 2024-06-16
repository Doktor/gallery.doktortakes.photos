from rest_framework import serializers

from photos.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("slug", "display_name", "description")
