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
from django.contrib.auth import authenticate

from .serializers import SignupSerializer, UserSerializer

class JWTSignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # jwt token 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입에 성공하였습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )
            # 쿠키에 넣어주기(set_cookie)
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JWTLoginView(APIView):
    def post(self, request):
        user = authenticate(
            user_id=request.data.get("user_id"), password=request.data.get("password")
        )
        if user is not None:
            serializer = UserSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "로그인에 성공하였습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status = status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

############################################################

class KakaoLoginView(APIView):
    def get(self, request):   
        access_token = request.GET.get('access_token', None) # access token 받기

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
                user_id = email.split(sep='@')[0],
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
        res = Response(
            {
                "user": nickname,
                "email": email,
                "profile_photo": profile_photo,
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
