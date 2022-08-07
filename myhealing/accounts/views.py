from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from myhealing.settings import SOCIAL_OUTH_CONFIG
import requests, json
from .models import Users
import urllib.request

class KakaoSignInView(APIView): # 인가코드 요청
    def get(self, request):
        client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
        kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        return redirect(
            f'{kakao_auth_api}&client_id={client_id}&redirect_uri={redirect_uri}'
        )

class KakaoCallBackView(APIView): # 토큰 요청
    def get(self, request):
        auth_code = request.GET.get('code')
        client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
       
        token_req = requests.get(f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={auth_code}')
        token_json = token_req.json()
        error = token_json.get('error')
        if error is not None:
            raise json.JSONDecodeError(error)

        access_token = token_json.get('access_token')


        profile_req = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"} # 사용자 정보 요청
        )

        # print(profile_json)    
        profile_json = profile_req.json() 

        return JsonResponse(data=profile_json, safe=False)
        