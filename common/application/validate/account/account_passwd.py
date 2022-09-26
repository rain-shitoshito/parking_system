import re
from ....domain.exceptions import PasswordException

class Password:
    
    def __init__(self, password, length=8):
        pattern = '\A(?=.*[A-Z])(?=.*[.?/-])[a-zA-Z0-9.?/-]{8,' + str(length) + '}\Z'

        if re.match(pattern, password):
            self.__password = password
        else:
            raise PasswordException('パスワードはアルファベット大文字・小文字・数字・記号少なくとも１文字含め8文字～{}文字で入力してください'.format(length))
        

    @property
    def password(self):
        return self.__password

    # パスワードが一致するか
    @staticmethod
    def compare(password, password_conf):
        if password != password_conf:
            raise PasswordException('パスワードが一致しません')
        return True

    # 新旧パスワードが不一致か
    @staticmethod
    def udt_compare(old_password, new_password):
        if old_password == new_password:
            raise PasswordException('旧パスワードと同一です')
        return True


    