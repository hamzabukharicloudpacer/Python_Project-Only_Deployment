from django.urls import path
from rest_framework import routers

from .views import index
from .viewsets import UserViewSet

routes = routers.SimpleRouter()
routes.register('', UserViewSet, basename='users')

urlpatterns = [
    path('index/', index)
]

urlpatterns += routes.urls
