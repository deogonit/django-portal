from django.test import TestCase
from django.urls import reverse, resolve


from ..models import Board
from ..views import BoardTopicsView


class BoardTopicsTest(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')

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
