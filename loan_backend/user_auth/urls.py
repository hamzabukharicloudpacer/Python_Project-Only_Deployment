from django.urls import path
from .views import (
    LoginView, LogoutView, ChangePasswordView, VerifyUsernameView,
    SendLinkView, VerifyResetPasswordLinkView, ResetPasswordView
)

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('verify_username/', VerifyUsernameView.as_view()),
    path('send_link/', SendLinkView.as_view()),
    path('verify_reset_password_link/', VerifyResetPasswordLinkView.as_view()),
    path('reset_password/', ResetPasswordView.as_view())
]
