from decimal import Decimal

from django.core.validators import EmailValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Loaner(models.Model):
    name = models.CharField(
        _('Name'),
        max_length=128
    )
    email = models.CharField(
        _('Email'),
        max_length=128,
        validators=[EmailValidator],
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('Phone'),
        max_length=32
    )
    address = models.CharField(
        _('Address'),
        max_length=1024,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
        related_name='loaners'
    )

    def __str__(self):
        return self.name


class Payment(models.Model):
    payment_amount = models.DecimalField(
        _('Payment Amount'),
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    payment_date = models.DateField(
        _('Payment Date')
    )
    RECEIVED = 'received'
    PAID = 'paid'
    PAYMENT_TYPES = [
        (RECEIVED, 'Received'),
        (PAID, 'Paid')
    ]
    payment_type = models.CharField(
        _('Payment Type'),
        max_length=10,
        choices=PAYMENT_TYPES,
        default=PAID
    )
    loaner = models.ForeignKey(
        Loaner,
        verbose_name=_('Loaner'),
        on_delete=models.CASCADE,
        related_name='payments'
    )
    is_pinned = models.BooleanField(
        _('Is Pinned'),
        default=False
    )

    def __str__(self):
        return f'({self.payment_amount}, {self.payment_date})'
