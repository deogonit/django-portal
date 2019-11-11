from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse, resolve


class PasswordChangeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='old_password')
        self.url = reverse('password_change')
        self.client.login(username='test', password='old_password')


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp()
        data = {
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        }
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        response = self.client.get(reverse('main_site'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp()
        data = {}
        self.response = self.client.post(self.url, data)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))