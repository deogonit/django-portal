from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from .forms import SignUpForm, UserForm, ProfileForm, SuperUserChangeRoleForm, AdminModerChangeRoleForm
from forum.models import Post


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
            return redirect('boards')
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):
    template_name = 'accounts/change_my_account.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
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
            return redirect('boards')
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
            'user': user
        }
        return render(request, self.template_name, context)


def create_page(request, objects, count_of_pages):
    paginator = Paginator(objects, count_of_pages)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)


class ListUsersView(View):
    template_name = 'accounts/users.html'

    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('pk')
        users = create_page(request, users, 10)
        context = {'page_objects': users}
        return render(request, self.template_name, context)


class ProfileView(View):
    template_name = 'accounts/account.html'

    def get(self, request, *args, **kwargs):
        form = None
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = self.get_ten_posts(user)
        if request.user.is_superuser:
            form = SuperUserChangeRoleForm(instance=user.profile)
        elif request.user.profile.is_moderator or user.profile.is_administrator:
            form = AdminModerChangeRoleForm(instance=user.profile)

        context = {
            'user_info': user,
            'form': form,
            'posts': posts
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = None
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = self.get_ten_posts(user)
        if request.user.is_superuser:
            form = SuperUserChangeRoleForm(request.POST, instance=user.profile)
        elif request.user.profile.is_moderator or request.user.profile.is_administrator:
            form = AdminModerChangeRoleForm(request.POST, instance=user.profile)
        if form is not None and form.is_valid():
            user_profile = form.save(commit=False)
            is_admin = form.cleaned_data['is_administrator']
            if is_admin:
                user_profile.is_moderator = True
            user_profile.save()
            return redirect('user_profile', username=user.username)
        context = {
            'user_info': user,
            'form': form,
            'posts': posts
        }
        return render(request, self.template_name, context)

    def get_ten_posts(self, user):
        posts = Post.objects.filter(created_by=user).order_by('-created_at')
        return posts[:10] if len(posts) > 10 else posts[:]
