from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from .exceptions import *
from django.contrib.auth import authenticate
from account.models import User
import common.domain.validate.account as vali_acc
from common.domain.intersepter import log_service

# ビジネスロジック
class AccountService:

    # 使用するモデルの格納
    def __init__(self, model):
        self.model = model


    # トークン検証
    @log_service('token_conf')
    def token_conf(self, token):
        try:
            timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
            user_pk = loads(token, max_age=timeout_seconds)
        except SignatureExpired:
            return False

        except BadSignature:
            return False
            
        else: 
            return user_pk


    # 仮のアカウント作成
    @log_service('prov_create')
    def prov_create(self, request, **validated_data):

        # ロジックバリデーション
        vali_acc.Email.email_conf(
            validated_data['email']
        )

        user = self.model.objects.create_user(
            validated_data['name'],
            validated_data['email'],
            validated_data['password'],
            validated_data['tel'],
        )

        current_site = get_current_site(request)
        domain = current_site.domain
        context = {
            'protocol': request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('account/mail_template/create/subject.txt', context)
        message = render_to_string('account/mail_template/create/message.txt', context)

        self.email_user(subject, message, None, [user.email])
        return user


    # アカウント有効化
    @log_service('prob_create')
    def prob_create(self, token):
        user_pk = self.token_conf(token)

        if user_pk:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return False
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save() 
                    return user
        else:
            return False


    # サインイン
    @log_service('signin')
    def signin(self, request, **validated_data):
        email = validated_data['email']
        password = validated_data['password']

        # ロジックバリデーション
        user = vali_acc.Password.registered_conf(
            request,
            email,
            password
        )
        if user is not None:
            login(request, user)
            return user
        else:

            return False


    # パスワード変更
    @log_service('update')
    def update(self, request, password_before, password_next):
        # ロジックバリデーション
        user = vali_acc.Password.registered_conf(
            request,
            request.user.email,
            password_before
        )
        user.set_password(password_next)
        user.save()
        user = authenticate(request, email=user.email, password=password_next)
        login(request, user)
        return user


    # emailへパスワードリセットメール送付
    @log_service('fg_update_send')
    def fg_update_send(self, request, email):

        # ロジックバリデーション
        user = vali_acc.Email.email_exist(email)

        current_site = get_current_site(request)
        domain = current_site.domain
        context = {
            'protocol': request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('account/mail_template/reset/subject.txt', context)
        message = render_to_string('account/mail_template/reset/message.txt', context)

        self.email_user(subject, message, None, [user.email])
        return True


    # パスワードを忘れたときメールアドレスから変更
    @log_service('fg_update')
    def fg_update(self, token, password):
        user_pk = self.token_conf(token)

        if user_pk:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return False
            else:
                user.set_password(password)
                user.save()
                return user
        else:
            return False


    # アカウント削除
    @log_service('destroy')
    def destroy(self, pk):
        user = User.objects.filter(pk=pk)
        if len(user) == 0:
            return False
        
        user.delete()
        return True


    # メール送信
    @log_service('email_user')
    def email_user(self, subject, message, from_email=None, to_email=[], **kwargs):
        send_mail(subject, message, from_email, to_email, **kwargs)


    