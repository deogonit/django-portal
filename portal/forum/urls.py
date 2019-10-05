from django.urls import path

from .views import BoardView, BoardTopicsView


urlpatterns = [
    path('', BoardView.as_view(), name='boards'),
    path('boards/<str:slug>/', BoardTopicsView.as_view(), name='board_topics'),

]
