from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login as auth_login

from .forms import SignUpForm


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
            auth_login(request, user)
            return redirect('main_site')
        return render(request, self.template_name, {'form': form})
