import sys
from django import forms
import common.application.validate.account as acc_validate
from common.domain.exceptions import *
from .models import User

# アカウント作成
class AccountCreateForm(forms.Form):

    name = forms.CharField(label='お名前', 
        widget=forms.TextInput(
            attrs={'placeholder':'お名前'}
        )
    )
    email = forms.CharField(label='メールアドレス', 
        widget=forms.TextInput(
            attrs={'placeholder':'メールアドレス'}
        )
    )
    email_conf = forms.CharField(label='メールアドレス確認', 
        widget=forms.TextInput(
            attrs={'placeholder':'メールアドレス（確認）'}
        )
    )
    tel = forms.CharField(label='電話番号', required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'電話番号'}
        )
    )
    password = forms.CharField(label='パスワード', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'パスワード'}
        )
    )
    password_conf = forms.CharField(label='パスワード確認',
        widget=forms.PasswordInput(
            attrs={'placeholder':'パスワード（確認）'}
        )
    )

    # nameバリデーション
    def clean_name(self):
        try:
            name = self.cleaned_data.get('name')
            vali = acc_validate.Name(name)
            return vali.name;
        except NameException as e:
            tb = sys.exc_info()[2]
            self.add_error('name', e.with_traceback(tb))


    # emailバリデーション
    def clean_email(self):
        try:
            email = self.cleaned_data.get('email')
            vali = acc_validate.Email(email)
            return vali.email
        except EmailException as e:
            tb = sys.exc_info()[2]
            self.add_error('email', e.with_traceback(tb))


    # telバリデーション
    def clean_tel(self):
        try:
            tel = self.cleaned_data.get('tel')
            if tel == '':
                return tel
            else:
                vali = acc_validate.Tel(tel)
                return vali.tel

        except TelException as e:
            tb = sys.exc_info()[2]
            self.add_error('tel', e.with_traceback(tb))


    # passwordバリデーション
    def clean_password(self):
        try:
            password = self.cleaned_data.get('password')
            vali = acc_validate.Password(password, 20)
            return vali.password
        except PasswordException as e:
            tb = sys.exc_info()[2]
            self.add_error('password', e.with_traceback(tb))


    # emailとパスワードの重複確認
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_conf = cleaned_data.get('email_conf')
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if email is None:
            email = ''
        if password is None:
            password = ''

        try:
            acc_validate.Email.compare(email, email_conf)
        except Exception as e:
            tb = sys.exc_info()[2]
            self.add_error('email_conf', e.with_traceback(tb))

        try:
            acc_validate.Password.compare(password, password_conf)
        except Exception as e:
            tb = sys.exc_info()[2]
            self.add_error('password_conf', e.with_traceback(tb))
        
        return cleaned_data


# ログイン
class AccountSignInForm(forms.Form):

    email = forms.CharField(label='メールアドレス', 
        widget=forms.TextInput(
            attrs={'placeholder':'メールアドレス'}
        )
    )

    password = forms.CharField(label='パスワード', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'パスワード'}
        )
    )

    # emailバリデーション
    def clean_email(self):
        try:
            email = self.cleaned_data.get('email')
            vali = acc_validate.Email(email)
            return vali.email
        except EmailException as e:
            tb = sys.exc_info()[2]
            self.add_error('email', e.with_traceback(tb))


    # passwordバリデーション
    def clean_password(self):
        try:
            password = self.cleaned_data.get('password')
            vali = acc_validate.Password(password, 20)
            return vali.password
        except PasswordException as e:
            tb = sys.exc_info()[2]
            self.add_error('password', e.with_traceback(tb))



# パスワード変更
class AccountPassChangeForm(forms.Form):

    password_before = forms.CharField(label='現在のパスワード', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'現在のパスワード'}
        )
    )

    password_next = forms.CharField(label='新しいパスワード', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'新しいパスワード'}
        )
    )

    password_conf = forms.CharField(label='新しいパスワード確認', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'新しいパスワード（確認）'}
        )
    )


    # password_beforeバリデーション
    def clean_password_before(self):
        try:
            password_before = self.cleaned_data.get('password_before')
            vali = acc_validate.Password(password_before, 20)
            return vali.password
        except PasswordException as e:
            tb = sys.exc_info()[2]
            self.add_error('password_before', e.with_traceback(tb))
        
    
    # password_nextバリデーション
    def clean_password_next(self):
        try:
            password_next = self.cleaned_data.get('password_next')
            vali = acc_validate.Password(password_next, 20)
            return vali.password
        except PasswordException as e:
            tb = sys.exc_info()[2]
            self.add_error('password_next', e.with_traceback(tb))
        

    # パスワードの重複確認
    def clean(self):
        cleaned_data = super().clean()
        password_before = cleaned_data.get('password_before')
        password_next = cleaned_data.get('password_next')
        password_conf = cleaned_data.get('password_conf')

        if password_before is None:
            password_before = ''

        if password_next is None:
            password_next = ''

        # 旧パスと新パスが一致
        try:
            acc_validate.Password.udt_compare(password_before, password_next)
        except Exception as e:
            tb = sys.exc_info()[2]
            self.add_error('password_next', e.with_traceback(tb))

        # 新パスと確認パスが不一致
        try:
            acc_validate.Password.compare(password_next, password_conf)

        except Exception as e:
            tb = sys.exc_info()[2]
            self.add_error('password_conf', e.with_traceback(tb))
        
        return cleaned_data


# パスワードを忘れたときメールアドレスから変更
class AccountEmailForm(forms.Form):
    email = forms.CharField(label='メールアドレス', 
        widget=forms.TextInput(
            attrs={'placeholder':'メールアドレス'}
        )
    )

    # emailバリデーション
    def clean_email(self):
        try:
            email = self.cleaned_data.get('email')
            vali = acc_validate.Email(email)
            return vali.email
        except EmailException as e:
            tb = sys.exc_info()[2]
            self.add_error('email', e.with_traceback(tb))



# パスワードを忘れた場合の変更
class AccountFgPassChangeForm(forms.Form):

    password_next = forms.CharField(label='新しいパスワード', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'新しいパスワード'}
        )
    )

    password_conf = forms.CharField(label='新しいパスワード確認', 
        widget=forms.PasswordInput(
            attrs={'placeholder':'新しいパスワード（確認）'}
        )
    )

    # password_nextバリデーション
    def clean_password_next(self):
        try:
            password_next = self.cleaned_data.get('password_next')
            vali = acc_validate.Password(password_next, 20)
            return vali.password
        except PasswordException as e:
            tb = sys.exc_info()[2]
            self.add_error('password_next', e.with_traceback(tb))
        

    # パスワードの重複確認
    def clean(self):
        cleaned_data = super().clean()
        password_next = cleaned_data.get('password_next')
        password_conf = cleaned_data.get('password_conf')

        if password_next is None:
            password_next = ''

        # 新パスと確認パスが不一致
        try:
            acc_validate.Password.compare(password_next, password_conf)

        except Exception as e:
            tb = sys.exc_info()[2]
            self.add_error('password_conf', e.with_traceback(tb))
        
        return cleaned_data

