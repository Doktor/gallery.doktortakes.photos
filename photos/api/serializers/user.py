from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from photos.api.fields import GroupField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    groups = GroupField(many=True, allow_empty=True, queryset=Q())

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'groups',
            'is_active', 'is_staff', 'is_superuser',
            'last_login', 'date_joined',
        )
        read_only_fields = (
            'username', 'is_staff', 'is_superuser',
        )
