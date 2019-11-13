from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .forms import SignUpForm, UserForm, ProfileForm


class SignUpView(View):
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_site')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):
    template_name = 'accounts/my_account.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'user': user
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('main_site')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'user': user
        }
        return render(request, self.template_name, context)
