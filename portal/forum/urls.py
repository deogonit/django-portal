from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import BoardView, BoardTopicsView, \
    TopicPostsView, NewTopicView, ReplyPostView, EditPostView, VotesView, DeletePostView, NewBoardView, EditTopicView, \
    DeleteTopicView
from .models import LikeDislike, Post

urlpatterns = [
    path('', BoardView.as_view(), name='boards'),
    path('boards/create', NewBoardView.as_view(), name='new_board'),
    path('boards/<str:slug>/', BoardTopicsView.as_view(), name='board_topics'),
    path('boards/<str:slug>/new_topic/', NewTopicView.as_view(), name='new_topic'),
    path('boards/<str:slug>/topics/<str:topic_slug>/', TopicPostsView.as_view(), name='topic_posts'),
    path('boards/<str:slug>/topics/<str:topic_slug>/edit', EditTopicView.as_view(), name='edit_topic'),
    path('boards/<str:slug>/topics/<str:topic_slug>/delete', DeleteTopicView.as_view(), name='delete_topic'),
    path('boards/<str:slug>/topics/<str:topic_slug>/post/<int:post_number>/like/',
         login_required(VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE)), name='post_like'),
    path('boards/<str:slug>/topics/<str:topic_slug>/post/<int:post_number>/dislike/',
         login_required(VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE)), name='post_dislike'),
    path('boards/<str:slug>/topics/<str:topic_slug>/', TopicPostsView.as_view(), name='topic_posts'),
    path('boards/<str:slug>/topics/<str:topic_slug>/reply/', ReplyPostView.as_view(), name='reply_post'),
    path('boards/<str:slug>/topics/<str:topic_slug>/post/<int:post_number>/edit/', EditPostView.as_view(),
         name='edit_post'),
    path('boards/<str:slug>/topics/<str:topic_slug>/post/<int:post_number>/delete/', DeletePostView.as_view(),
         name='delete_post'),
]
