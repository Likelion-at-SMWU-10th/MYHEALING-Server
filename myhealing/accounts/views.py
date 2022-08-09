from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse

from .serializers import UserJWTSignupSerializer


class JWTSignupView(APIView):
    serializer_class = UserJWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)

            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)

            return JsonResponse(
                                {'user': user,
                                 'token': {'access': access_token,
                                           'refresh': refresh_token},
                                },
                                status=status.HTTP_200_OK,
                               )
        else:
            return JsonResponse({'msg': 'token issuance error'})