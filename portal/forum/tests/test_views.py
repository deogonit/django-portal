from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board
from ..views import BoardView


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


class BoardTopicsTest(TestCase):
    def setUp(self) -> None:
        Board.objects.create(name='Test name', description='Test description')
        self.slug = 'test-name'

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'slug': self.slug})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_contains_navigation_links(self):
        board_topics_url = reverse('board_topics', kwargs={'slug': self.slug})
        board_url = reverse('boards')
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{}"'.format(board_url))

    def test_board_topics_view_uses_correct_template(self):
        response = self.client.get(reverse('board_topics', kwargs={'slug': self.slug}))
        self.assertTemplateUsed(response, 'forum/board_topics.html')