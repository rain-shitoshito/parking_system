from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import generic
from common.domain.intersepter import *
from django.contrib.auth import get_user_model

User =  get_user_model()

# マイページ
class ClientMypage(YouOrSuperMixin, generic.TemplateView):
    template_name = 'client/mypage.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = User.objects.get(pk=pk)
        ctx = {
            'user': user
        }
        return render(request, 'client/mypage.html', ctx)
