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

    def test_boards_view_function(self):
        view = resolve('/forum/')
        self.assertEquals(view.func.view_class, BoardView)

