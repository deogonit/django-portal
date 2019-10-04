from django.shortcuts import render

from .models import Board


def board_view(request):
    boards = Board.objects.all()
    return render(request, 'forum/boards.html', context={
        'boards': boards
    })
