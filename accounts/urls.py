from django.urls import path
from .views import UserProfileView, UpdateProfilePassword, UserRegistrationView, VerifyUserLinkView, LoginView, \
    ResetPasswordView, CreateNewPasswordView

#app_name='accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_password/', UpdateProfilePassword.as_view(), name='update_password'),
    path('create-account', VerifyUserLinkView.as_view(), name='create_account'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('forgot-password', VerifyUserLinkView.as_view(), name='forgot_password'),
    path('create-new-password', CreateNewPasswordView.as_view(), name='create_new_password'),
]
