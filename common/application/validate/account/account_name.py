from ....domain.exceptions import *

class Name:
    
    def __init__(self, name, length=20):
        if not len(name) <= length:
            raise NameException('名前は{}文字以内で入力してください'.format(length))
        self.__name = name
            

    @property
    def name(self):
        return self.__name

