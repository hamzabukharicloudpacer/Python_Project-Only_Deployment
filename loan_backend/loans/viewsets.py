import collections

from django.db.models import Sum, Q, F, Case, Value, When
from rest_framework import viewsets, response, filters
from rest_framework.decorators import action

from loan_backend.shared.mixins import MultipleSerializersViewSetMixin
from .filters import PaymentFilterSet
from .models import Loaner, Payment
from .serializers import (
    LoanerSerializer, PaymentCreateOrUpdateSerializer, PaymentListOrDetailSerializer
)


class LoanersViewSet(MultipleSerializersViewSetMixin, viewsets.ModelViewSet):
    serializer_class = LoanerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Loaner.objects.filter(user=self.request.user).order_by('name')

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        return super(LoanersViewSet, self).create(request, *args, **kwargs)


class PaymentsViewSet(MultipleSerializersViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PaymentCreateOrUpdateSerializer
    serializers = {
        'list': PaymentListOrDetailSerializer,
        'retrieve': PaymentListOrDetailSerializer,
        'partial_update': PaymentCreateOrUpdateSerializer,
        'metadata': PaymentCreateOrUpdateSerializer
    }
    filterset_class = PaymentFilterSet

    def get_queryset(self):
        return Payment.objects.filter(
            loaner__user=self.request.user
        ).order_by(
            '-payment_date', 'loaner__name'
        )

    def list(self, request, *args, **kwargs):
        super_response = super(PaymentsViewSet, self).list(request, *args, **kwargs)
        payments_list = super_response.data
        filtered_queryset = self.filter_queryset(self.get_queryset())
        query_set = filtered_queryset.aggregate(
            received=Sum('payment_amount', filter=Q(payment_type=Payment.RECEIVED)),
            paid=Sum('payment_amount', filter=Q(payment_type=Payment.PAID)),
        )
        response_data = collections.OrderedDict(
            received_amount=query_set.get('received'),
            paid_amount=query_set.get('paid'),
            payments=payments_list
        )
        return response.Response(response_data)

    @action(methods=['PATCH'], detail=True)
    def pin_to_dashboard(self, request, pk):
        payment = self.get_object()
        payment.is_pinned = Case(
            When(is_pinned=True, then=Value(False)),
            default=Value(True)
        )

        payment.save()
        serializer = self.get_serializer(payment)
        return response.Response(
            serializer.data
        )
