from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..models import Board, Topic, Post
from ..views import TopicPostsView


class TopicPosts(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')
        user = User.objects.create_user(username='john', email="vlas@mail.com", password='123')
        self.topic = Topic.objects.create(name='Test topic', board=self.board, who_started_topic=user)
        Post.objects.create(message='Test message', topic=self.topic, created_by=user)
        self.url = reverse('topic_posts', kwargs={'slug': self.board.slug, 'topic_slug': self.topic.slug})
        self.response = self.client.get(self.url)

    def test_board_topics_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_board_topics_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'forum/topic_posts.html')

    def test_boards_view_function(self):
        view = resolve('/forum/boards/{}/topics/{}/'.format(self.board.slug, self.topic.slug))
        self.assertEquals(view.func.view_class, TopicPostsView)
