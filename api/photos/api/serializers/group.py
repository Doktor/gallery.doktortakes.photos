from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import serializers

from photos.api.fields import UserField


class GroupSerializer(serializers.ModelSerializer):
    users = UserField(many=True, allow_empty=True, queryset=Q(), source='user_set')

    class Meta:
        model = Group
        fields = ('id', 'name', 'users')
        read_only_fields = ('name',)
