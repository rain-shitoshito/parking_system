from ast import Pass
import re
import copy
from unittest import TestCase
from common.domain.exceptions import *
from django.contrib.auth import get_user_model
import common.application.validate.account as app_validate
import common.domain.validate.account as dmn_validate


class TestAppValiUser(TestCase):

    def test_email(self):
        vali = app_validate.Email
        # 成功
        vali('test@gmail.com')

        # 失敗
        faild_list = [
            'test',
            'test@hogehoge'
            'test@gmail.'
            'test@yahoo.co.'
        ]

        for i in faild_list:
            try:
                vali(i)
            except EmailException:
                assert True
            else:
                assert False
        
        #compare
        self.assertEquals(
            vali.compare(
                'test@gmail.com',
                'test@gmail.com'
            ),
            True
        )

        try:
            vali.compare(
                'test@gmail.com',
                'hoge@gmail.com'
            )

        except EmailException:
            assert True
        else:
            assert False
        
        

    def test_name(self):
        vali = app_validate.Name

        # 成功
        vali(
            'テストテストテストテストテストテストテス'
        )

        # 失敗
        try:
            vali(
                'テストテストテストテストテストテストテスト'
            )
        
        except NameException:
            assert True
        
        else:
            assert False


    def test_password(self):
        vali = app_validate.Password

        success_list = [
            'Testtest00-',
            'Testtest00----------'
        ]
        # 成功
        for i in success_list:
            try:
                vali(i, 20)

            except PasswordException:
                assert False
            
            else:
                assert True



        faild_list = [
            'testTest',
            'test',
            'test01123123',
            'testTest00-----------'
            'test--/'
        ]

        for i in faild_list:
            try:
                vali(i, 20)
            except PasswordException:
                assert True
            else:
                assert False


    def test_tel(self):
        vali = app_validate.Tel

        vali(
            '00000000000'
        )

        try:
            failed_list = [
                '000000000'
                '000-0000-0000'
            ]

            for i in failed_list:
                vali(i)
        
        except TelException:
            assert True
        
        else:
            assert False
