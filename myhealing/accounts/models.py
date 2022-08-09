from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, user_id, password, email, nickname, introduce, profile_photo, header_photo, **kwargs):
        """
        주어진 개인정보로 일반 User 인스턴스 생성
        """       
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_id = user_id,
            email = email,
            nickname = nickname,
            introduce = introduce,
            profile_photo = profile_photo,
            header_photo = header_photo,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, email, nickname, introduce, profile_photo, header_photo, ):
        """
        주어진 개인정보로 관리자 User 인스턴스 생성
        최상위 사용자이므로 권한 부여
        """
        user = self.create_user(
            user_id = user_id,
            email = email,
            nickname = nickname,
            introduce = introduce,
            profile_photo = profile_photo,
            header_photo = header_photo,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(unique=True, blank=False, max_length=15)
    email = models.CharField(unique=True, blank=False, max_length=255)
    nickname = models.CharField(unique=True, blank=False, max_length=15)
    introduce = models.CharField(blank=True, max_length=50)
    profile_photo = models.ImageField(blank=True, max_length=400)
    header_photo = models.ImageField(blank=True, max_length=400)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


# class User(models.Model):
#     user_id = models.CharField(max_length=15)
#     password = models.CharField(max_length=15)
#     email = models.CharField(max_length=255)
#     nickname = models.CharField(max_length=15)
#     introduce = models.CharField(max_length=50)
#     profile_photo = models.ImageField(name="프로필 이미지", upload_to="img/accounts/", height_field=None, width_field=None, max_length=400, blank=True)
#     header_photo = models.ImageField(name="배경 이미지", upload_to="img/accounts/", height_field=None, width_field=None, max_length=400, blank=True)