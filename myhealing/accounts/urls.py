from django.urls import path
from .views import KakaoSignInView

urlpatterns = [
    path('', KakaoSignInView.as_view())
]