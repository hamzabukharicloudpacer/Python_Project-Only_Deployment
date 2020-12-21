from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from loan_backend.users.models import User
from .models import ResetPasswordLink


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        label=_('Username')
    )
    password = serializers.CharField(
        required=True,
        label=_('Password'),
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(
        required=True,
        label=_('Current Password'),
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        label=_('New Password'),
        style={'input_type': 'password'}
    )

    def validate_current_password(self, password):
        request = self.context.get('request')
        if not request.user.check_password(password):
            msg = _('Current password is not correct.')
            raise serializers.ValidationError(msg)
        return password


class VerifyUserNameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            msg = _('No user exists with this username.')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class SendResetPasswordLinkSerializer(VerifyUserNameSerializer):
    email = serializers.EmailField(required=True)


class VerifyResetPasswordLinkSerialzer(serializers.Serializer):
    link_token = serializers.CharField(required=True)

    def validate(self, attrs):
        link_token = attrs.get('link_token')
        error_msg = _('The link token is not valid')

        try:
            reset_password = ResetPasswordLink.objects.get(link_token=link_token)
        except ResetPasswordLink.DoesNotExist:
            raise serializers.ValidationError(error_msg)
        if reset_password.expiry_time <= now():
            reset_password.delete()
            raise serializers.ValidationError(error_msg)

        attrs['user'] = reset_password.user
        return attrs


class ResetPasswordSerializer(VerifyResetPasswordLinkSerialzer):
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
