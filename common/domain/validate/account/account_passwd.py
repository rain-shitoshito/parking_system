from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from ...exceptions import PasswordException

class Password:

    User = get_user_model()
    
    # パスワードが自身のものか
    @staticmethod
    def registered_conf(request, email, password):

        user = authenticate(request, email=email, password=password)

        if user:
            return user
        else:
            raise PasswordException('パスワードが間違っています')
