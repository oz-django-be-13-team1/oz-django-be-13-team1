from __future__ import annotations

import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("올바른 이메일 주소를 작성주세요.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            #비밀번호 없이 만들 일 없으면 강제 요구 가능
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self,email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise  ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column='user_id',
    )

    email =models.EmailField("이메일",max_length=255,unique=True,db_column='email')
    nickname = models.CharField("닉네임",max_length=50, db_column='nickname')
    name = models.CharField("이름",max_length=50, db_column='name')

    phone_regex = RegexValidator(
        regex=r"^\-?1?\d{1,20}$",
        message="전화번호는 - 포함한 최대 20자리 숫자 형식이어야합니다.",
    )
    phone_number = models.CharField(
        "전화번호", max_length=20, validators=[phone_regex], blank=True,db_column='phone_number'
    )

    last_login = models.DateTimeField("마지막 로그인", blank=True,null=True,db_column='last_login')

    is_staff = models.BooleanField("스태프 여부", default=timezone.now, db_column='is_staff')
    is_admin = models.BooleanField("관리자 플래그",default=False, db_column='is_admin')
    is_active = models.BooleanField("활성화 여부", default=True,db_column='is_active')

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname','name']

    class Meta:
        db_table = 'users'
        verbose_name = '유저'
        verbose_name_plural = '유저'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['nickname']),
            models.Index(fields=['phone_number']),
        ]

        def __str__(self) -> str:
            return f"{self.email} ({self.nickname})"