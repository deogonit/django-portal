from django.urls import path

from .views import BoardView, BoardTopicsView, \
    TopicPostsView, NewTopicView, ReplyPostView, EditPostView

urlpatterns = [
    path('', BoardView.as_view(), name='boards'),
    path('boards/<str:slug>/', BoardTopicsView.as_view(), name='board_topics'),
    path('boards/<str:slug>/new_topic', NewTopicView.as_view(), name='new_topic'),
    path('boards/<str:slug>/topics/<str:topic_slug>/', TopicPostsView.as_view(), name='topic_posts'),
    path('boards/<str:slug>/topics/<str:topic_slug>/reply', ReplyPostView.as_view(), name='reply_post'),
    path('boards/<str:slug>/topics/<str:topic_slug>/post/<int:post_number>/edit', EditPostView.as_view(),
         name='edit_post')
]
