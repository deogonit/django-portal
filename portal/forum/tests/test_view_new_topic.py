from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..models import Board, Topic, Post
from ..views import NewTopicView
from ..forms import NewTopicForm


class NewTopicTests(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')
        self.user = User.objects.create_user(username='john', email="vlas@mail.com", password='123')
        self.client.login(username='john', password='123')

    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'slug': 'simple-slug'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_topic_contains_link_to_back_to_boards_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'slug': self.board.slug})
        board_topics_url = reverse('board_topics', kwargs={'slug': self.board.slug})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{}"'.format(board_topics_url))

    def test_csrf(self):
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_contains_form(self):
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_post_valid_data(self):
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        data = {}
        response = self.client.post(url, data)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_topic_post_invalid_data(self):
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        data = {
            'name': 'Test topic',
            'message': 'Test topic message'
        }
        self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_post_empty_fields(self):
        url = reverse('new_topic', kwargs={'slug': self.board.slug})
        data = {
            'name': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
