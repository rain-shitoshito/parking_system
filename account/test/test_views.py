from multiprocessing import set_forkserver_preload
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from django.core.signing import loads, dumps
from django.contrib.auth import authenticate
import datetime
from ..views import *
from ..forms import *
from ..models import *

# URLとViewが一致しているか

class TestUrls(TestCase):

    # signup/
    def test_signup(self):
        url = reverse('account:signup')
        self.assertEqual(resolve(url).func.view_class, AccountSignUp)
    
    # signup-done/
    def test_signup(self):
        url = reverse('account:signup_done')
        self.assertEqual(resolve(url).func.view_class, AccountSignUpDone)
    
    # signup-complete/<str:token>/
    def test_signup_complete(self):
        url = reverse('account:signup_complete', kwargs=dict(token='hoge'))
        self.assertEqual(resolve(url).func.view_class, AccountSignUpComplete)
    
    # pass-update/<int:pk>/
    def test_pass_update(self):
        url = reverse('account:pass_update', kwargs=dict(pk='1'))
        self.assertEqual(resolve(url).func.view_class, AccountPassUpdate)
    
    # signin/
    def test_signin(self):
        url = reverse('account:signin')
        self.assertEqual(resolve(url).func.view_class, AccountSignin)
    
    # signout/
    def test_signout(self):
        url = reverse('account:signout')
        self.assertEqual(resolve(url).func.view_class, AccountSignout)
    
    # fgpass-update-email/
    def test_fgpass_update_email(self):
        url = reverse('account:fgpass_update_email')
        self.assertEqual(resolve(url).func.view_class, AccountFgPassUpdateEmail)
    
    # fgpass-update-email-done/
    def test_fgpass_update_email_done(self):
        url = reverse('account:fgpass_update_email_done')
        self.assertEqual(resolve(url).func.view_class, AccountFgPassUpdateEmailDone)
    
    # fgpass-update/<str:token>/
    def test_fgpass_update(self):
        url = reverse('account:fgpass_update', kwargs=dict(token='hoge'))
        self.assertEqual(resolve(url).func.view_class, AccountFgPassUpdate)
    
    # fgpass-update-complete/
    def test_fgpass_update_complete(self):
        url = reverse('account:fgpass_update_complete')
        self.assertEqual(resolve(url).func.view_class, AccountFgPassUpdateEmailComplete)


# signup/
class TestSignup(TestCase):

    def setUp(self):
        self.User = get_user_model()

    # 成功するGETのテスト
    def test_get_success(self):
        response = self.client.get(reverse('account:signup'))

        # ステータスコードが200か
        self.assertEqual(response.status_code, 200)
        
        # テンプレートが正しいものか
        self.assertTemplateUsed(response, 'account/signup.html')
        
        # レスポンスのコンテキストが正しいか
        self.assertContains(response, 'form')
        
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountCreateForm)


    # 成功するPOSTのテスト
    def test_post_success(self):
        params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'email_conf': 'test@gmail.com',
            'tel': '09000000000',
            'password': 'Testtest01-',
            'password_conf': 'Testtest01-'
        }

        response = self.client.post(reverse('account:signup'), params)

        # リダイレクト先のテンプレートが正しいか
        # リダイレクト先のステータスコードが正しいか
        # リダイレクト元のステータスコードが正しいか
        self.assertRedirects(
            response, 
            reverse('account:signup_done'), 
            status_code=302, 
            target_status_code=200, 
            msg_prefix='', 
            fetch_redirect_response=True
        )
        # DBに作成したアカウントが存在するか
        self.assertEqual(self.User.objects.filter(email=params['email']).count(), 1)

    
    # 失敗するPOSTのテスト
    def test_post_failed(self):

        params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'email_conf': 'test@gmail.com',
            'tel': '09000000000',
            'password': 'Testtest01-',
            'password_conf': 'Testtest01-'
        }

        # 予め同じメールアドレスのユーザを作成
        self.User.objects.create_user(
            name = params['name'],
            email = params['email'],
            password = params['password'],
            tel = params['tel']
        )

        response = self.client.post(reverse('account:signup'), params)

        # ステータスコードが200か
        self.assertEqual(response.status_code, 200)
        
        # テンプレートが正しいものか
        self.assertTemplateUsed(response, 'account/signup.html')

        # レスポンスのコンテキストが正しいか
        self.assertContains(response, 'form')

# signup-done/
class TestSignUpDone(TestCase):

    # テンプレートが正しいものか
    def test_get_success(self):
        response = self.client.get(reverse('account:signup_done'))
        self.assertTemplateUsed(response, 'account/signup_done.html')


# signup-complete/<str:token>/
class TestSignUpComplete(TestCase):

    def setUp(self):
        self.User = get_user_model()

    # 成功するGETのテスト
    def test_get_success(self):
        params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'email_conf': 'test@gmail.com',
            'tel': '09000000000',
            'password': 'Testtest01-',
            'password_conf': 'Testtest01-'
        }

        # ユーザを作成
        user = self.User.objects.create_user(
            name = params['name'],
            email = params['email'],
            password = params['password'],
            tel = params['tel']
        )
        
        response = self.client.get(reverse('account:signup_complete', kwargs=dict(token=dumps(user.pk))))

        # ステータスコードが200か
        self.assertEqual(response.status_code, 200)
        # テンプレートが正しいものか
        self.assertTemplateUsed(response, 'account/signup_complete.html')
    
    
    # 失敗するGETのテスト
    def test_get_failed(self):
        response = self.client.get(reverse('account:signup_complete', kwargs=dict(token='hoge')))
        self.assertEqual(response.status_code, 400)
    

# signin/
class TestSignIn(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'email_conf': 'test@gmail.com',
            'tel': '09000000000',
            'password': 'Testtest01-',
            'password_conf': 'Testtest01-'
        }

        # ユーザを作成
        self.user = self.User.objects.create_user(
            name = self.params['name'],
            email = self.params['email'],
            password = self.params['password'],
            tel = self.params['tel']
        )
        self.user.is_active = True
        self.user.save()
    

    # 成功するGETのテスト
    def test_get_success(self):
        response = self.client.get(reverse('account:signin'))

        # ステータスコードが200か
        self.assertEqual(response.status_code, 200)
        
        # テンプレートが正しいものか
        self.assertTemplateUsed(response, 'account/signin.html')
        
        # レスポンスのコンテキストが正しいか
        self.assertContains(response, 'form')
        
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountSignInForm)


    # 成功するPOSTのテスト
    def test_post_success(self):

        response = self.client.post(
            reverse('account:signin'), 
            {
                'email': self.params['email'],
                'password': self.params['password']
            }
        )

        # リダイレクト先のテンプレートが正しいか
        # リダイレクト先のステータスコードが正しいか
        # リダイレクト元のステータスコードが正しいか
        self.assertRedirects(
            response, 
            reverse('client:mypage', kwargs=dict(pk=self.user.pk)), 
            status_code=302, 
            target_status_code=200, 
            msg_prefix='', 
            fetch_redirect_response=True
        )

        # セッションIDが付与されているか
        assert response.cookies['sessionid'].OutputString()


    # 失敗するPOSTのテスト
    def test_post_failed(self):
        response = self.client.post(
            reverse('account:signin'), 
            {
                'email': self.params['email'],
                'password': 'testpass'
            }
        )

        # テンプレートが正しいものか
        self.assertTemplateUsed(response, 'account/signin.html')
        
        # レスポンスのコンテキストが正しいか
        self.assertContains(response, 'form')

    
# signout/
class TestSignOut(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'email_conf': 'test@gmail.com',
            'tel': '09000000000',
            'password': 'Testtest01-',
            'password_conf': 'Testtest01-'
        }

        # ユーザを作成
        self.user = self.User.objects.create_user(
            name = self.params['name'],
            email = self.params['email'],
            password = self.params['password'],
            tel = self.params['tel']
        )
        self.user.is_active = True
        self.user.save()
    

    # 成功するGETのテスト
    def test_get_success(self):
        # ログインする
        self.client.force_login(self.user)

        response = self.client.get(reverse('client:mypage', kwargs=dict(pk=self.user.pk)))
        
        # ログインできているか
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/mypage.html')

        response = self.client.get(reverse('account:signout'))

        # ステータスコードが200か
        self.assertEqual(response.status_code, 200)
        
        # テンプレートが正しいものか
        self.assertTemplateUsed(response, 'account/signout.html')
        
        # セッションクッキーが破棄されているか
        assert response.cookies['sessionid'].value == ''


# pass-update/<int:pk>/
class TestPassUpdate(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'password': 'Testtest01-',
            'tel': '09000000000'
        }

        # ユーザを作成
        self.user = self.User.objects.create_user(
            name = self.params['name'],
            email = self.params['email'],
            password = self.params['password'],
            tel = self.params['tel']
        )
        self.user.is_active = True
        self.user.save()
    

    # 成功するGETのテスト
    def test_get_success(self):
        # ログインする
        self.client.force_login(self.user)
        
        response = self.client.get(reverse('account:pass_update', kwargs=dict(pk=self.user.pk)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/password_change.html')

        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountPassChangeForm)


    # 失敗するGETのテスト
    def test_get_failed(self):
        response = self.client.get(reverse('account:pass_update', kwargs=dict(pk=self.user.pk)))
        # 403アクセス禁止
        self.assertEqual(response.status_code, 403)


    # 成功するPOSTのテスト
    def test_post_success(self):
        # ログインする
        self.client.force_login(self.user)
        params = {
            'password_before': self.params['password'],
            'password_next': 'Testtest01--',
            'password_conf': 'Testtest01--'
        }
        response = self.client.post(
            reverse('account:pass_update', kwargs=dict(pk=self.user.pk)), 
            params
        )

        # ユーザのパスワードが更新されたか
        assert isinstance(
            authenticate(email=self.params['email'], password=params['password_next']),
            self.User
        )


    # 失敗するPOSTのテスト
    def test_post_failed(self):
        # ログインする
        self.client.force_login(self.user)

        # 元のパスワードが違う
        response = self.client.post(
            reverse('account:pass_update', kwargs=dict(pk=self.user.pk)), 
            {
                'password_before': 'hogehoge',
                'password_next': 'Testtest01--',
                'password_conf': 'Testtest01--'
            }
        )
        self.assertEqual(response.status_code, 200)
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountPassChangeForm)

        # 新しいパスワードと確認パスワードが違う
        response = self.client.post(
            reverse('account:pass_update', kwargs=dict(pk=self.user.pk)), 
            {
                'password_before': self.params['password'],
                'password_next': 'Testtest01--',
                'password_conf': 'Testtest01-'
            }
        )
        self.assertEqual(response.status_code, 200)
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountPassChangeForm)


# fgpass-update-email/
class TestFgPassUpdateEmail(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'password': 'Testtest01-',
            'tel': '09000000000'
        }

        # ユーザを作成
        self.user = self.User.objects.create_user(
            name = self.params['name'],
            email = self.params['email'],
            password = self.params['password'],
            tel = self.params['tel']
        )
        self.user.is_active = True
        self.user.save()

    # 成功するGETのテスト
    def test_get_success(self):
        response = self.client.get(reverse('account:fgpass_update_email'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/etpassword_send.html')
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountEmailForm)
        
    # 成功するPOSTのテスト
    def test_post_success(self):

        response = self.client.post(
            reverse('account:fgpass_update_email'), 
            {
                'email': self.params['email']
            }
        )
    
        # リダイレクト先のテンプレートが正しいか
        # リダイレクト先のステータスコードが正しいか
        # リダイレクト元のステータスコードが正しいか
        self.assertRedirects(
            response, 
            reverse('account:fgpass_update_email_done'), 
            status_code=302, 
            target_status_code=200, 
            msg_prefix='', 
            fetch_redirect_response=True
        )
    
    # 失敗するPOSTのテスト
    def test_post_failed(self):

        # 存在しないemailを送信
        response = self.client.post(
            reverse('account:fgpass_update_email'), 
            {
                'email': 'notexist@gmail.com'
            }
        )

        self.assertTemplateUsed(response, 'account/etpassword_send.html')
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountEmailForm)


# fgpass-update-email-done/
class TestFgPassUpdateEmailDone(TestCase):

    def test_get_success(self):
        response = self.client.get(reverse('account:fgpass_update_email_done'))
        self.assertTemplateUsed(response, 'account/etpassword_done.html')


# fgpass-update/<str:token>/
class TestFgPassUpdate(TestCase):

    def setUp(self):
        self.User = get_user_model()
        self.params = {
            'name': 'テスト',
            'email': 'test@gmail.com',
            'password': 'Testtest01-',
            'tel': '09000000000'
        }

        # ユーザを作成
        self.user = self.User.objects.create_user(
            name = self.params['name'],
            email = self.params['email'],
            password = self.params['password'],
            tel = self.params['tel']
        )
        self.user.is_active = True
        self.user.save()

    # 成功するGETのテスト
    def test_get_success(self):
        response = self.client.get(reverse('account:fgpass_update', kwargs=dict(token=dumps(self.user.pk))))
        # テンプレートが正しいか
        self.assertTemplateUsed(response, 'account/etpassword_change.html')
        # コンテキストに含まれるフォームが正しいか
        self.assertEqual(response.context['form'].__class__, AccountFgPassChangeForm)



    # 失敗するGETのテスト
    def test_get_failed(self):
        response = self.client.get(reverse('account:fgpass_update', kwargs=dict(token='badtoken')))
        self.assertEqual(response.status_code, 400)


# fgpass-update-complete/
class TestFgPassUpdateEmailComplete(TestCase):

    # 成功するGETのテスト
    def test_get_success(self):
        response = self.client.get(reverse('account:fgpass_update_complete'))
        self.assertTemplateUsed(response, 'account/etpassword_complete.html')

