from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from photos.api.fields import GroupField

User = get_user_model()


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=200, write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise ValidationError("Missing username or password.")

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if user is None:
            raise ValidationError("Invalid username or password.")

        data['user'] = user
        return data


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
