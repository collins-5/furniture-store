from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import loginForm

from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('index1', views.index1, name='index1'),
    path('sold/', views.sold, name='sold'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.auth_view, name='login'),  # Combined login/signup view
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('logout/', views.logout_view, name='logout'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-use/', views.terms_of_use, name='terms_of_use'),
    path('faq/', views.faq, name='faq'),
    path('about/', views.about, name='about'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
