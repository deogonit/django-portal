from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import ModelForm

from ..models import Board, Topic, Post
from ..views import EditPostView


class EditPostViewTestCase(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')
        self.user = User.objects.create_user(username='john', email="vlas@mail.com", password='123')
        self.topic = Topic.objects.create(name='Test topic', board=self.board, who_started_topic=self.user)
        self.post = Post.objects.create(message='Test post', topic=self.topic, created_by=self.user)
        self.url = reverse('edit_post', kwargs={
            'slug': self.board.slug,
            'topic_slug': self.topic.slug,
            'post_number': self.post.pk
        })


class EditPostViewTests(EditPostViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 302)


class SuccessfulEditPostViewTests(EditPostViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username='john', password='123')
        data = {
            'message': 'Test message'
        }
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        topic_post_url = reverse('topic_posts', kwargs={'slug': self.board.slug, 'topic_slug': self.topic.slug})
        self.assertRedirects(self.response, topic_post_url)

    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'Test message')


class InvalidEditPostViewTests(EditPostViewTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username='john', password='123')
        data = {}
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)