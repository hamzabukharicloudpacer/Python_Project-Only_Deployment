from django_filters import rest_framework as filterset

from loan_backend.loans.models import Payment


class PaymentFilterSet(filterset.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'loaner__name': ['icontains'],
            'loaner_id': ['exact'],
            'payment_date': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'payment_amount': ['exact', 'lt', 'gt', 'lte', 'gte'],
            'payment_type': ['exact'],
        }
