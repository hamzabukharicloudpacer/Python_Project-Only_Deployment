import collections

from django.db.models import F, Sum, Q
from rest_framework import response, views

from loan_backend.loans.models import Payment
from .serializers import PinnedPaymentSerialzer


class DashboardView(views.APIView):

    def get(self, request, *args, **kwargs):
        response_data = collections.OrderedDict({
            **self.get_total_paid_and_received(),
            'pinned_payments': self.get_pinned_payments()
        })
        return response.Response(response_data)

    def get_pinned_payments(self):
        pinned_payments = Payment.objects.annotate(
            payment_loaner=F('loaner__name')
        ).filter(
            loaner__user=self.request.user,
            is_pinned=True
        )
        payments_serializer = PinnedPaymentSerialzer(pinned_payments, many=True)
        return payments_serializer.data

    def get_total_paid_and_received(self):
        paid_received = Payment.objects.filter(
            loaner__user=self.request.user
        ).aggregate(
            received=Sum(
                'payment_amount',
                filter=Q(payment_type=Payment.RECEIVED)
            ),
            paid=Sum('payment_amount', filter=Q(payment_type=Payment.PAID))
        )
        paid_received.update({
            'payments_difference':
                (paid_received.get('received') or 0) -
                (paid_received.get('paid') or 0)
        })
        return paid_received
