from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from myhealing.settings import SOCIAL_OUTH_CONFIG
import requests, json
from .models import User
import urllib.request

"""
인가코드 요청
"""
class KakaoSignInView(APIView):
    def get(self, request):
        client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
        kakao_auth_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
        return redirect(
            f'{kakao_auth_api}&client_id={client_id}&redirect_uri={redirect_uri}'
        )


class KakaoCallBackView(APIView):
    def get(self, request):
        auth_code = request.GET.get('code')
        client_id = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
        redirect_uri = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
       
        """
        토큰 요청
        """
        token_req = requests.get(f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={auth_code}')
        token_json = token_req.json()
        error = token_json.get('error')
        if error is not None:
            raise json.JSONDecodeError(error)

        access_token = token_json.get('access_token') # access token 추출

        """
        사용자 정보(profile) 요청
        """
        profile_req = requests.get(
            "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"}
        )

        # print(profile_json)    
        profile_json = profile_req.json()
        email = profile_json.get("kakao_account").get("email") # email 값
        properties = profile_json.get("kakao_account").get("profile")
        nickname = properties.get("nickname") # 이름값
        profile_photo = properties.get("profile_image_url") # 프로필 사진
        header_photo = properties.get("thumbnail_image_url") # 헤더(배경) 사진
        # return JsonResponse(data=properties, safe=False)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(
                email = email,
                nickname = nickname,
            )
            # user.set_unusable_password()
            user.save()
            if profile_photo is not None: # kakao profile에 image가 있다면
                profile_photo_req = requests.get(profile_photo)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(profile_photo_req.content)
                )
        login(request, user)
        return redirect(reverse('kakaologin')) # redirect page는 추후 변경.


class KakaoFinishView(APIView):
    def get(self, request):
        data = {
            'message' : 'kakao login success!'
        }
        return JsonResponse(data=data)