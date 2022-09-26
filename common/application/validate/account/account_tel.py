import re
from ....domain.exceptions import TelException

class Tel:
    
    def __init__(self, tel, length=8):
        pattern = '\A\d{10,}\Z'
        if not re.match(pattern, tel):
            raise TelException('数字のみで電話番号を入力してください。')
        self.__tel = tel

    @property
    def tel(self):
        return self.__tel
