from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class UserManager(BaseUserManager):
    use_in_migrations: True

    def create_user(self, user_id, password, email, nickname, introduce, profile_photo, **kwargs):
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
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_id, password, **extra_fields):
        """
        주어진 개인정보로 관리자 User 인스턴스 생성
        최상위 사용자이므로 권한 부여
        """
        user = self.create_user(
            user_id = user_id,
            email = email,
            nickname = user_id,
            password = password,
            introduce = None,
            profile_photo = None,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    avatar = models.ImageField(upload_to="img/avatar/", blank=True, null=True)
    user_id = models.CharField(unique=True, blank=False, null=False, max_length=15, default='')
    email = models.CharField(unique=True, blank=False, null=False, max_length=255)
    nickname = models.CharField(unique=True, blank=False, null=False, max_length=15, default='')
    introduce = models.CharField(blank=True, null=True,  max_length=50)
    profile_photo = models.ImageField(blank=True, null=True,  max_length=400)
    last_login = models.DateField(auto_now=True, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 user id로 설정
    USERNAME_FIELD = 'user_id'
    # 필수 작성 field
    REQUIRED_FIELDS = ['email']

# class KakaoUser(models.Model):
#     avatar = models.ImageField(upload_to="img/avatar/", blank=True, null=True)
#     email = models.CharField(max_length=255)
#     nickname = models.CharField(max_length=15)
#     introduce = models.CharField(max_length=50, blank=True, null=True)
#     profile_photo = models.TextField(blank=True, null=True)
#     last_login = models.DateField(auto_now=True, null=True)