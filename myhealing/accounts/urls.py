from django.urls import path
from .views import KakaoSignInView, KakaoCallBackView

urlpatterns = [
    path('kakao/', KakaoSignInView.as_view()),
    path('accounts/kakao/login/callback/', KakaoCallBackView.as_view())
]