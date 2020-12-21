import binascii
import datetime
import os
import secrets

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class UserSession(models.Model):
    token = models.CharField(
        _('Token'),
        max_length=512
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_sessions',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    start_time = models.DateTimeField(
        _('Start Time'),
        auto_now_add=True
    )
    expiry_time = models.DateTimeField(
        verbose_name=_('Expiry Time'),
        default=None
    )

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        if not self.expiry_time:
            self.expiry_time = now() + datetime.timedelta(days=7)
        return super().save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.token


class ResetPasswordLink(models.Model):
    link_token = models.CharField(
        _('Link Token'),
        max_length=256
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='reset_password_link',
        on_delete=models.CASCADE, verbose_name=_("User")
    )
    expiry_time = models.DateTimeField(
        verbose_name=_('Expiry Time'),
        default=None
    )

    def save(self, *args, **kwargs):
        if not self.link_token:
            self.link_token = self.generate_token()
        if not self.expiry_time:
            self.expiry_time = now() + datetime.timedelta(minutes=5)
        return super().save(*args, **kwargs)

    def generate_token(self):
        return secrets.token_urlsafe(64)
