from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('mypage/<int:pk>/', views.ClientMypage.as_view(), name='mypage'),
]

