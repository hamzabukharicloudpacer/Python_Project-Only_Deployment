from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class PinnedPaymentSerialzer(serializers.Serializer):
    id = serializers.IntegerField(
        label=_('Payment ID')
    )
    payment_type = serializers.CharField(
        label=_('Payment Type')
    )
    payment_amount = serializers.DecimalField(
        label=_('Payment Amount'),
        max_digits=12,
        decimal_places=2
    )
    payment_date = serializers.DateField(
        label=_('Payment Date')
    )
    payment_loaner = serializers.CharField(
        label=_('Payment Loaner')
    )
