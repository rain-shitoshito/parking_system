from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views import generic
from .forms import *
from .models import *
from common.domain.intersepter import *
from common.domain.account_service import AccountService

# ユーザ作成（仮）
class AccountSignUp(generic.FormView):
    form_class = AccountCreateForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:prov_create')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = {
            'form': self.form_class()
        }

    def form_valid(self, form):
        try:
            service = AccountService(User)
            
            result = service.prov_create(
                self.request, 
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                tel = form.cleaned_data['tel'],
                password = form.cleaned_data['password']
            )
        except EmailException as e:
            tb = sys.exc_info()[2]
            form.add_error('email', e.with_traceback(tb))
            self.ctx['form'] = form
            return render(self.request, self.template_name, self.ctx)

        else:
            return redirect('account:signup_done')


# ユーザ作成（仮）完了
class AccountSignUpDone(generic.TemplateView):
    template_name = 'account/signup_done.html'


# ユーザ作成完了
class AccountSignUpComplete(generic.TemplateView):
    template_name = 'account/signup_complete.html'

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        service = AccountService(User)

        result = service.prob_create(token)

        if result:
            return super().get(request, **kwargs)
        else:
            return HttpResponseBadRequest()


# サインイン
class AccountSignin(generic.FormView):
    template_name = 'account/signin.html'
    form_class = AccountSignInForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = {
            'form': self.form_class()
        }

    def form_valid(self, form):
        try:
            service = AccountService(User)
            user = service.signin(
                self.request,
                email = form.cleaned_data['email'],
                password = form.cleaned_data['password']
            )

        except PasswordException as e:
            tb = sys.exc_info()[2]
            form.add_error('password', e.with_traceback(tb))
            self.ctx['form'] = form
            return render(self.request, self.template_name, self.ctx)

        else:
            return redirect('client:mypage', pk=user.pk)


# サインアウト
class AccountSignout(generic.TemplateView):
    template_name = 'account/signout.html'

    def get(self, request, *args, **kwargs):
        request.session.flush()
        return super().get(request, *args, **kwargs)


# パスワード更新
class AccountPassUpdate(YouOrSuperMixin, generic.TemplateView):
    form_class = AccountPassChangeForm
    template_name = 'account/password_change.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = {
            'form': self.form_class()
        }


    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name, self.ctx)


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        # ロジックバリデーションはここで行いたい
        if form.is_valid():
            try:
                service = AccountService(User)
                result = service.update(
                    request, 
                    form.cleaned_data['password_before'], 
                    form.cleaned_data['password_next']
                )

            except PasswordException as e:
                tb = sys.exc_info()[2]
                form.add_error('password_before', e.with_traceback(tb))
            else:
                #通知メッセージ
                messages.success(self.request, 'パスワードを更新しました。')

        self.ctx['form'] = form
        return render(self.request, self.template_name, self.ctx)



# emailへパスワードリセットメール送付
class AccountFgPassUpdateEmail(generic.FormView):
    template_name = 'account/etpassword_send.html'
    form_class = AccountEmailForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx = {
            'form': self.form_class()
        }


    def form_valid(self, form):
        email = form.cleaned_data['email']
        service = AccountService(User)
        try:
            result = service.fg_update_send(self.request, email)

        except EmailException as e:
            tb = sys.exc_info()[2]
            form.add_error('email', e.with_traceback(tb))
            self.ctx['form'] = form
            return render(self.request, self.template_name, self.ctx)

        else:
            return redirect('account:fgpass_update_email_done')


# パスワードリセットメール送付完了
class AccountFgPassUpdateEmailDone(generic.TemplateView):
    template_name = 'account/etpassword_done.html'


# emailからパスワードリセット
class AccountFgPassUpdate(generic.FormView):
    template_name = 'account/etpassword_change.html'
    form_class = AccountFgPassChangeForm

    def get(self, request, **kwargs):
        token = kwargs.get('token')
        service = AccountService(User)

        result = service.token_conf(token)

        if result:
            return super().get(request, **kwargs)
        else:
            return HttpResponseBadRequest()


    def form_valid(self, form):
        service = AccountService(User)
        result = service.fg_update(
            self.kwargs['token'],
            form.cleaned_data['password_next']
        )

        if result:
            return redirect('account:fgpass_update_complete')
        else:
            return HttpResponseBadRequest()


# パスワードリセット送付完了
class AccountFgPassUpdateEmailComplete(generic.TemplateView):
    template_name = 'account/etpassword_complete.html'
