from django.urls import path
from accounts import views

urlpatterns = [
    path('kakaoLoginLogic/', views.kakaoLoginLogic, name='kakaoLoginLogic'),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect, name='kakaoLoginLogicRedirect'),
    path('kakaoLogout/', views.kakaoLogout, name='kakaoLogout'),
]