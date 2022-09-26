from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .repositorys import *


# Create your models here.

# ユーザモデル
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(help_text='名前', max_length=20)
    email = models.CharField(help_text='メールアドレス', unique=True, max_length=40)
    password = models.CharField(help_text='パスワード', max_length=128)
    tel = models.CharField(help_text='電話番号', null=True, blank=True, unique=True, max_length=11)
    date_joind = models.DateTimeField(help_text='登録日時')
    is_active = models.BooleanField(help_text='有効/無効', default=False)
    is_superuser = models.BooleanField(help_text='一般ユーザ/スーパーユーザ', default=False)

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'ユーザモデル'
        verbose_name_plural = 'ユーザモデル'

    def __str__(self):
        return self.email

