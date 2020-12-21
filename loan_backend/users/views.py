from rest_framework.decorators import api_view, permission_classes
from rest_framework import response, permissions


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def index(request):
    return response.Response({
        'message': 'This is the test endpoint.'
    })
