from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.AccountSignUp.as_view(), name='signup'),
    path('signup-done/', views.AccountSignUpDone.as_view(), name='signup_done'),
    path('signup-complete/<str:token>/', views.AccountSignUpComplete.as_view(), name='signup_complete'),
    path('pass-update/<int:pk>/', views.AccountPassUpdate.as_view(), name='pass_update'),
    path('signin/', views.AccountSignin.as_view(), name='signin'),
    path('signout/', views.AccountSignout.as_view(), name='signout'),
    path('fgpass-update-email/', views.AccountFgPassUpdateEmail.as_view(), name='fgpass_update_email'),
    path('fgpass-update-email-done/', views.AccountFgPassUpdateEmailDone.as_view(), name='fgpass_update_email_done'),
    path('fgpass-update/<str:token>/', views.AccountFgPassUpdate.as_view(), name='fgpass_update'),
    path('fgpass-update-complete/', views.AccountFgPassUpdateEmailComplete.as_view(), name='fgpass_update_complete'),
]

