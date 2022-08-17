from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import *

urlpatterns = [
    path('signup/', JWTSignupView.as_view()), # 회원가입
    path('login/', JWTLoginView.as_view()), # 로그인
    path('login/refresh/', TokenRefreshView.as_view()), # 토큰 재발급
    path('accounts/kakao/accesstoken/<str:access_token>', KakaoCallBackView.as_view()),
]