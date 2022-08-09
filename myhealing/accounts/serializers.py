from tkinter.ttk import Style
from rest_framework import serializers
from .models import User

class UserJWTSignupSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(write_only=True, max_length=15)
    password = serializers.CharField(write_only=True, max_length=15)
    email = serializers.CharField(write_only=True, max_length=255)
    nickname = serializers.CharField(write_only=True, max_length=15)
    introduce = serializers.CharField(write_only=True, max_length=50)
    profile_photo = serializers.ImageField(required=False, max_length=400)
    header_photo = serializers.ImageField(required=False, max_length=400)
    
    class Meta(object):
        model = User
        fields = ['user_id', 'password', 'email', 'nickname', 'introduce', 'profile_photo', 'header_photo']

        def save(self, request):
            user = super().save()

            user.user_id = self.validated_data['user_id']
            user.password = self.validated_data['password']
            user.email = self.validated_data['email']
            user.nickname = self.validated_data['nickname']
            user.introduce = self.validated_data['introduce']
            user.profile_photo = self.validated_data['profile_photo']
            user.header_photo = self.validated_data['header_photo']

            user.save()

            return user

        def validate(self, data):
            user_id = data.get('user_id', None)

            if User.objects.filter(user_id=user_id).exits():
                raise serializers.ValidationError("이미 존재하는 사용자입니다.")

            return data