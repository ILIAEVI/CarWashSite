from django.urls import path
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView

)
from . import views
from authentication.views import CustomPasswordResetView

urlpatterns = [
    path("", views.index, name='home'),
    path("login/", views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path("logout/", views.user_logout, name='logout'),
    path("activate/<str:uidb64>/<str:token>/", views.email_activate, name='activate'),
    path(
        'password-reset/',
        CustomPasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'password_reset_confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'password_reset_complete/',
        PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'
    ),
]
