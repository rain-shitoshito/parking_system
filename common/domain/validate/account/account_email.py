from django.contrib.auth import get_user_model
from ...exceptions import EmailException

class Email:

    User = get_user_model()

    
    # ユーザ名（email)の重複確認
    @staticmethod
    def email_conf(email):
        try:
            user = Email.User.objects.filter(email=email).get()
        except Email.User.DoesNotExist:
            return True
        else:
            raise EmailException('存在するメールアドレスです')


    # ユーザ名(email)が存在する
    @staticmethod
    def email_exist(email):
        try:
            user = Email.User.objects.filter(email=email).get()
        except Email.User.DoesNotExist:
            raise EmailException('存在しないメールアドレスです')
        else:
            return user
