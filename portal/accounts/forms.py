from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.EmailInput()
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False
    )
    last_name = forms.CharField(
        max_length=50,
        required=False
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False,)

    class Meta:
        model = UserProfile
        fields = ('avatar',)