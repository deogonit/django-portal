from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase

from ..views import SignUpView
from ..forms import SignUpForm

class SignUpTests(TestCase):
    def setUp(self) -> None:
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func.view_class, SignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)


class SuccessfulSignUpTests(TestCase):
    def setUp(self) -> None:
        url = reverse('signup')
        data = {
            'username': 'deogonit',
            'email': 'site@gmail.com',
            'password1': 'abcdefgh123',
            'password2': 'abcdefgh123',
        }
        self.response = self.client.post(url, data)
        self.redirect_url = reverse('main_site')

    def test_redirection(self):
        self.assertRedirects(self.response, self.redirect_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response = self.client.get(self.redirect_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self) -> None:
        url = reverse('signup')
        self.response = self.client.post(url, data={})

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())