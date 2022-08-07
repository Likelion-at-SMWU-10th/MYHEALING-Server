from django.db import models

class Users(models.Model):
    user_id = models.BigIntegerField()
    email = models.CharField(max_length=255)
    nickname = models.CharField(max_length=15)
    introduce = models.CharField(max_length=50, blank=True)
    profile_photo = models.TextField(blank=True)
    header_photo = models.TextField(blank=True)