from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..models import Board, Topic, Post
from ..views import BoardView, BoardTopicsView, TopicPostsView


class BoardsTests(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')

    def test_boards_view_status_code(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_boards_view_url_by_name(self):
        response = self.client.get(reverse('boards'))
        self.assertEquals(response.status_code, 200)

    def test_boards_view_uses_correct_template(self):
        response = self.client.get(reverse('boards'))
        self.assertTemplateUsed(response, 'forum/boards.html')

    def test_boards_view_function(self):
        view = resolve('/forum/')
        self.assertEquals(view.func.view_class, BoardView)


class BoardTopicsTest(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name='Test name', description='Test description')
        self.board = Board.objects.first()

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'slug': self.board.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'slug': self.board.slug})
        board_url = reverse('boards')
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{}"'.format(board_url))

    def test_board_topics_view_uses_correct_template(self):
        response = self.client.get(reverse('board_topics', kwargs={'slug': self.board.slug}))
        self.assertTemplateUsed(response, 'forum/board_topics.html')

    def test_boards_view_function(self):
        view = resolve('/forum/boards/{}/'.format(self.board.slug))
        self.assertEquals(view.func.view_class, BoardTopicsView)


class TopicPosts(TestCase):
    def setUp(self) -> None:
        board = Board.objects.create(name='Test name', description='Test description')
        self.board_slug = Board.objects.first()
        user = User.objects.create_user(username='john', email="vlas@mail.com", password='123')
        topic = Topic.objects.create(name='Test topic', board=board, who_started_topic=user)
        self.topic_slug = Topic.objects.first()
        Post.objects.create(message='Test message', topic=topic, created_by=user)
        self.url = reverse('topic_posts', kwargs={'slug': board.slug, 'topic_slug': topic.slug})
        self.response = self.client.get(self.url)

    def test_board_topics_view_success_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_board_topics_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'forum/topic_posts.html')

    def test_boards_view_function(self):
        view = resolve('/forum/boards/{}/topics/{}/'.format(self.board_slug, self.topic_slug))
        self.assertEquals(view.func.view_class, TopicPostsView)

    # TODO: 1. Add test for creating models, forms and new views
    # TODO: 2. Split tests into separate files
