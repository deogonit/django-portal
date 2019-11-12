from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

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
            login(request, user)
            return redirect('main_site')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/my_account.html'
    success_url = reverse_lazy('settings')

    def get_object(self, **kwargs):
        return self.request.user
