from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..models import Board, Topic, Post
from ..views import ReplyPostView
from ..forms import PostForm


class ReplyTopicTestCase(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')
        self.user = User.objects.create_user(username='john', password='123')
        self.topic = Topic.objects.create(name='Test topic', board=self.board, who_started_topic=self.user)
        Post.objects.create(message='Test message', topic=self.topic, created_by=self.user)
        self.url = reverse('reply_post', kwargs={'slug': self.board.slug, 'topic_slug': self.topic.slug})


class ReplyTopicTest(ReplyTopicTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username='john', password='123')
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/forum/boards/{}/topics/{}/reply')
        self.assertEquals(view.func.view_class, ReplyPostView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<textarea', 1)


class SuccessfulReplyTopicTests(ReplyTopicTestCase):
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

    def test_post_created(self):
        self.assertEquals(Post.objects.count(), 2)


class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username='john', password='123')
        data = {}
        self.response = self.client.post(self.url, data)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)