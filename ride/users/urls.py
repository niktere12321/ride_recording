from django.conf.urls import url
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('edd_user/<str:username>/', views.edd_user, name='edd_user'),
    path('users_help/', views.users_help, name='users_help'),
    path('help_active/', views.help_active, name='help_active'),
    path('add_new_user/', views.add_new_user, name='add_new_user'),
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/<str:new_email>/', views.SignUp, name='signup'),
    path(
        'login/',
        LoginView.as_view
        (template_name='users/login.html'),
        name='login'),
    path(
        'password_reset_form/',
        PasswordResetView.as_view
        (email_template_name='users/password_reset_email.html',template_name='users/password_reset_form.html',success_url='/users/password_reset/done/'),
        name='password_reset_form'),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view
        (template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    url(
        r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view
        (template_name='users/password_reset_confirm.html',success_url='/users/password_reset_complete/'),
        name='password_reset_confirm'),
    path(
        'password_reset_complete/',
        PasswordResetCompleteView.as_view
        (template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),
    path(
        'password_change_form/',
        PasswordChangeView.as_view
        (template_name='users/password_change_form.html'),
        name='password_change'),
    path(
        'password_change_done/',
        PasswordChangeDoneView.as_view
        (template_name='users/password_change_done.html'),
        name='password_change_done'),
]
