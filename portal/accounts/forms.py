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
    avatar = forms.ImageField(required=False, widget=forms.FileInput())
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Enter description about yourself'
            }),
        max_length=100,

    )

    class Meta:
        model = UserProfile
        fields = ('avatar', 'description')


class SuperUserChangeRoleForm(forms.ModelForm):
    is_administrator = forms.BooleanField(required=False)
    is_moderator = forms.BooleanField(required=False)

    class Meta:
        model = UserProfile
        fields = ['is_administrator', 'is_moderator']
        labels = {
            'is_administrator': 'Admin',
            'is_moderator': 'Moder'
        }


class AdminModerChangeRoleForm(forms.ModelForm):
    is_moderator = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = UserProfile
        fields = ['is_moderator', ]
