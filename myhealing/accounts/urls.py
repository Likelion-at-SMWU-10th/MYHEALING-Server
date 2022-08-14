from django.urls import path
from .views import KakaoSignInView, KakaoCallBackView, KakaoFinishView

urlpatterns = [
    path('kakao/', KakaoSignInView.as_view()),
    path('accounts/kakao/login/callback/', KakaoCallBackView.as_view()),
    path('kakao/login/finish/', KakaoFinishView.as_view(), name='kakaologin'),
]