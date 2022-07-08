from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id_token = models.CharField(max_length=100) # 사용자 식별 Kakao ID
    provider = models.CharField(max_length=10) # Naver, Kakao, Google
    photo_url = models.CharField(blank=True, max_length=100)
