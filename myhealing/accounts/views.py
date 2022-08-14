from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.core.files.base import ContentFile
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from myhealing.settings import SOCIAL_OUTH_CONFIG
import requests, json
from .models import User

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
        # return JsonResponse(data=properties, safe=False)
        try: # DB에 email이 존재하는지 확인
            user = User.objects.get(email=email)
        except User.DoesNotExist: # DB에 없다면 계정 생성
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
        # jwt token 접근
        token = TokenObtainPairSerializer.get_token(user)
        jwt_refresh_token = str(token)
        jwt_access_token = str(token.access_token)
        # profile_photo_req = requests.get(profile_photo)
        res = Response(
            {
                "user": nickname,
                "email": email,
                # "profile_photo": ContentFile(profile_photo_req.content, encoding='utf-16'),
                "message": "카카오 로그인에 성공하였습니다.",
                "token": {
                    "access": jwt_access_token,
                    "refresh": jwt_refresh_token,
                },
            },
            status = status.HTTP_200_OK
        )
        res.set_cookie("access", jwt_access_token, httponly=True)
        res.set_cookie("refresh", jwt_refresh_token, httponly=True)
        return res
        # return redirect(reverse('kakaologin')) # redirect page는 추후 변경.


class KakaoFinishView(APIView):
    def get(self, request):
        data = {
            'message' : 'kakao login success!'
        }
        return JsonResponse(data=data)