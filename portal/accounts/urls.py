from django.urls import path
from .views import SignUpView
from django.contrib.auth.views import LogoutView, LoginView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
