from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Board
from ..views import board_view


class BoardsTests(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name='Test name', description='Test description')
        url = reverse('boards')
        self.response = self.client.get(url)

    def test_boards_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_boards_url_resolves_boards_view(self):
        view = resolve('/forum/')
        self.assertEquals(view.func, board_view)