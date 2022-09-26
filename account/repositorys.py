from .models import *
from django.contrib.auth.models import UserManager
import datetime

class CustomUserManager(UserManager):

    use_in_migrations = True

    # ユーザ作成ベース
    def _create_user(self, name, email, password, tel, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, tel=tel, **extra_fields)
        user.set_password(password)
        user.date_joind = datetime.datetime.now()
        user.save()
        return user


    # ユーザ作成
    def create_user(self, name, email, password, tel, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, email, password, tel, **extra_fields)

    # Adminユーザ作成
    def create_superuser(self, name, email, password, tel, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, email, password, tel, **extra_fields)


