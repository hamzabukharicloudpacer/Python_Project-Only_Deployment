from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from .models import UserSession


class SessionTokenAuthentication(BaseAuthentication):
    token_prefix = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.token_prefix.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            user_session = UserSession.objects.select_related('user').get(token=token)
        except UserSession.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if user_session.expiry_time <= timezone.now():
            user_session.delete()
            raise exceptions.AuthenticationFailed(_('Session token has expired.'))

        if not user_session.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        return user_session.user, None
