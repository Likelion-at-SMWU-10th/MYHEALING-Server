from django.db import models

class User(models.Model):
    avatar = models.ImageField(upload_to="img/avatar/", blank=True, null=True)
    email = models.CharField(max_length=255)
    nickname = models.CharField(max_length=15)
    introduce = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.TextField(blank=True, null=True)
    last_login = models.DateField(auto_now=True, null=True)