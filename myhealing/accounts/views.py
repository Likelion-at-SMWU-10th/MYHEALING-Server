from django.shortcuts import render, redirect
from rest_framework.views import APIView
from myhealing.settings import SOCIAL_OUTH_CONFIG
import requests

class KakaoSignInView(APIView):
    def get(self, request):
        client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
        kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        return redirect(
            f'{kakao_auth_api}&client_id={client_id}&redirect_uri={redirect_uri}'
        )
