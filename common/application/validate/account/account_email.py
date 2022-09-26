import re
from ....domain.exceptions import EmailException

class Email:
    
    def __init__(self, email):
        pattern = '\A[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\Z'
        if not re.match(pattern, email):
            raise EmailException('メールアドレスを入力してください')
        self.__email = email

    @property
    def email(self):
        return self.__email

    @staticmethod
    def compare(email, email_conf):
        print(email)    
        if email != email_conf:
            raise EmailException('メールアドレスが一致しません')
        return True