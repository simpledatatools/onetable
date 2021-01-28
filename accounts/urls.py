from django.urls import path
from .views import UserRegisterView, UserProfileView, UpdateProfilePassword

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_password/', UpdateProfilePassword.as_view(), name='update_password'),
]
