from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import *

urlpatterns = [
    path('signup/', JWTSignupView.as_view()),
]