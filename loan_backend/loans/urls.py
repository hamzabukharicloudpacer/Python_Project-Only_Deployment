from rest_framework import routers

from .viewsets import LoanersViewSet, PaymentsViewSet

routes = routers.SimpleRouter()
routes.register('loaners', LoanersViewSet, basename='loaners')
routes.register('payments', PaymentsViewSet, basename='payments')

urlpatterns = routes.urls
