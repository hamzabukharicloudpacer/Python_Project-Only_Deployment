from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Loaner, Payment


class LoanerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loaner
        fields = '__all__'


class PaymentLoanerSerializer(LoanerSerializer):
    class Meta(LoanerSerializer.Meta):
        fields = ['id', 'name']


class PaymentCreateOrUpdateSerializer(serializers.ModelSerializer):
    payment_type = serializers.ChoiceField(
        label=_('Payment Type'),
        required=True,
        choices=[
            (Payment.PAID, 'Paid'),
            (Payment.RECEIVED, 'Received')
        ]
    )

    def validate_loaner(self, value):
        request = self.context.get('request')
        if value.user.id != request.user.id:
            msg = _('Loaner value is not valid.')
            raise serializers.ValidationError(msg)
        return value

    class Meta:
        model = Payment
        exclude = ['is_pinned']


class PaymentListOrDetailSerializer(serializers.ModelSerializer):
    loaner = PaymentLoanerSerializer(
        label=_('Loaner')
    )

    class Meta:
        model = Payment
        fields = '__all__'
