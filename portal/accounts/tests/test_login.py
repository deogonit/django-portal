from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm


class LogInTests(TestCase):
    def setUp(self) -> None:
        url = reverse('login')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/login/')
        self.assertEquals(view.func.view_class, LoginView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)

    def test_form_has_fields(self):
        form = AuthenticationForm()
        expected = ['username', 'password']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class SuccessfulSignUpTests(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(username='test', password='12345678asd')
        url = reverse('login')
        data = {
            'username': 'test',
            'password': '12345678asd',
        }
        self.response = self.client.post(url, data)
        self.redirect_url = reverse('main_site')

    def test_redirection(self):
        self.assertRedirects(self.response, self.redirect_url)

    def test_user_authentication(self):
        response = self.client.get(self.redirect_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self) -> None:
        url = reverse('login')
        self.response = self.client.post(url, data={})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)