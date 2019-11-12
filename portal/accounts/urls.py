from django.urls import path, include
from .views import SignUpView
from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetCompleteView, PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView

from .views import UserUpdateView

account_patterns = ([
    path('settings', UserUpdateView.as_view(), name='settings'),
    path('password/', PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),
    path('password/done/',
         PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done')
])


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'), name='password_reset'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/', PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('account/', include(account_patterns)),
]

