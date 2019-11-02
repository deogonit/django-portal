from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..models import Board, Topic, Post
from ..views import DeletePostView


class DeletePostTestCase(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')
        self.user = User.objects.create_user(username='john', email="vlas@mail.com", password='123')
        self.topic = Topic.objects.create(name='Test topic', board=self.board, who_started_topic=self.user)
        self.post = Post.objects.create(message='Test post', topic=self.topic, created_by=self.user)
        self.url = reverse('delete_post', kwargs={
            'slug': self.board.slug,
            'topic_slug': self.topic.slug,
            'post_number': self.post.pk
        })
        self.client.login(username='john', password='123')


class DeletePostViewTests(DeletePostTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.response = self.client.get(self.url)

    def test_new_topic_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_new_topic_view_not_found_status_code(self):
        url = reverse('delete_post', kwargs={
            'slug': 'simple-slug',
            'topic_slug': 'simple-slug',
            'post_number': 99
        })
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_contains_link_to_boards_topics_view(self):
        board_topics_url = reverse('board_topics', kwargs={'slug': self.board.slug})
        self.assertContains(self.response, 'href="{}"'.format(board_topics_url))

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')


class SuccessfulDeletePostTests(DeletePostTestCase):
    def setUp(self) -> None:
        super().setUp()
        data = {
            'post_number': self.post.pk
        }
        self.response = self.client.post(self.url, data)

    def test_redirection(self):
        topic_post_url = reverse('topic_posts', kwargs={'slug': self.board.slug, 'topic_slug': self.topic.slug})
        self.assertRedirects(self.response, topic_post_url)

    def test_exist_post(self):
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())