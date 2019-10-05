from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Board


class BoardView(View):
    template_name = 'forum/boards.html'

    def get(self, request, *args, **kwargs):
        boards = Board.objects.all()
        context = {
            'boards': boards
        }
        return render(request, self.template_name, context)


class BoardTopicsView(View):
    template_name = 'forum/board_topics.html'

    def get(self, request, slug):
        board = get_object_or_404(Board, slug__iexact=slug)
        context = {
            'board': board
        }
        return render(request, self.template_name, context)
