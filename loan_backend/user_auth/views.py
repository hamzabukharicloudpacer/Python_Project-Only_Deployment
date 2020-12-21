from django.core.mail import send_mail
from rest_framework import generics, response, permissions, views, status

from loan_backend.users.serializers import UserSerializer
from .models import UserSession, ResetPasswordLink
from .serializers import (
    LoginSerializer, ChangePasswordSerializer, SendResetPasswordLinkSerializer,
    VerifyUserNameSerializer, VerifyResetPasswordLinkSerialzer, ResetPasswordSerializer
)


def _get_session_token(request):
    return request.META.get('HTTP_AUTHORIZATION').split()[1]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        session_token = UserSession.objects.create(user=user)
        user_serializer = UserSerializer(user)
        return response.Response({
            'token': session_token.token,
            'user': user_serializer.data
        })


class LogoutView(views.APIView):

    def post(self, request, *args, **kwargs):
        session_token = _get_session_token(self.request)
        UserSession.objects.get(token=session_token).delete()
        return response.Response(status=status.HTTP_200_OK)


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data.get('new_password'))
        request.user.save()
        session_token = _get_session_token(request)
        request.user.user_sessions.exclude(token=session_token).delete()
        return response.Response(status=status.HTTP_200_OK)


class VerifyUsernameView(generics.GenericAPIView):
    serializer_class = VerifyUserNameSerializer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.query_params,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return response.Response({
            'email': user.email
        })


class SendLinkView(generics.GenericAPIView):
    serializer_class = SendResetPasswordLinkSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.email = serializer.validated_data['email']
        link = ResetPasswordLink.objects.create(user=user)
        email_message = """
                Hello, {},

                Please, use this link to reset your password.


                http://localhost:4200/accounts/reset-password/{}

                Please, note that the link will expire after five minutes.

                Kind Regards,
                Team Loan Management
                """.format(user.get_full_name(), link.link_token)
        send_mail(
            'Password Reset Link',
            email_message,
            'm.muaaz.nu@gmail.com',
            [user.email]
        )
        user.save()
        return response.Response(status=status.HTTP_200_OK)


class VerifyResetPasswordLinkView(generics.GenericAPIView):
    serializer_class = VerifyResetPasswordLinkSerialzer
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.query_params,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        user.user_sessions.all().delete()
        user.reset_password_link.all().delete()
        return response.Response(status=status.HTTP_200_OK)
