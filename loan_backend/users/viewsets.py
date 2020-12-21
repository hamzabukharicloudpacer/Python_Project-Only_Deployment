from rest_framework import viewsets, permissions, response, status
from rest_framework.decorators import action

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=['OPTIONS', 'POST'],
        permission_classes=[permissions.AllowAny]
    )
    def register(self, request):
        return self.create(request=request)

    @action(
        detail=False,
        methods=['OPTIONS', 'GET'],
    )
    def me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)

    @action(
        detail=False,
        methods=['OPTIONS', 'PATCH'],
    )
    def edit_me(self, request):
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)

    @action(
        detail=False,
        methods=['OPTIONS', 'DELETE'],
    )
    def delete_me(self, request):
        self.request.user.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
