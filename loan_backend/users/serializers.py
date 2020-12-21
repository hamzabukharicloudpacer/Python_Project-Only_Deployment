from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        label=_('Password'),
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(
        required=True
    )
    last_name = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        return User.objects.create_user(username, is_superuser=True, **validated_data)
