import re
import datetime
from unittest import TestCase
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from ..models import *


class TestRepositoryUser(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'password': 'Testtest01-',
            'tel': '09000000000'
        }
    
    # _create_user(ユーザ作成ベース)
    def test_baseuser_create(self):

        user = self.User.objects._create_user(
            name = self.params['name'], 
            email = self.params['email'], 
            password = self.params['password'], 
            tel = self.params['tel']
        )

        # name
        self.assertEquals(user.name, self.params['name'])
        # email
        self.assertEquals(user.email, self.params['email'])
        # tel
        self.assertEquals(user.tel, self.params['tel'])

        # password
        self.assertEqual(check_password(self.params['password'], user.password), True)

        # date_joind
        pattern = '^[0-9]{4}\-[0-9]{2}\-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}$'

        if not re.match(pattern, str(user.date_joind)):
            assert False

        self.User.objects.get(pk=user.pk).delete()


    # create_user(ユーザ作成)
    def test_user_create(self):

        user = self.User.objects.create_user(
            name = self.params['name'], 
            email = self.params['email'], 
            password = self.params['password'], 
            tel = self.params['tel']
        )

        # is_active
        self.assertEqual(user.is_active, False)

        # is_superuser
        self.assertEqual(user.is_superuser, False)

        self.User.objects.get(pk=user.pk).delete()


    # create_superuser(Adminユーザ作成)
    def test_superuser_create(self):
        user = self.User.objects.create_superuser(
            name = self.params['name'], 
            email = self.params['email'], 
            password = self.params['password'], 
            tel = self.params['tel']
        )

        # is_active
        self.assertEqual(user.is_active, True)

        # is_superuser
        self.assertEqual(user.is_superuser, True)

        self.User.objects.get(pk=user.pk).delete()

