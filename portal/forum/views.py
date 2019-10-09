from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Board, Topic, Post
from .forms import NewTopicForm, ReplyPostForm


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


class TopicPostsView(View):
    template_name = 'forum/topic_posts.html'

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic,
                                  board__slug=self.kwargs.get('slug'),
                                  slug=self.kwargs.get('topic_slug')
                                  )
        posts = topic.posts.all()
        context = {
            'topic': topic,
            'posts': posts
        }
        return render(request, self.template_name, context)


class NewTopicView(View):
    template_name = 'forum/new_topic.html'

    def get(self, request, *args, **kwargs):
        form = NewTopicForm()
        board = get_object_or_404(Board, slug=self.kwargs.get('slug'))
        context = {
            'board': board,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        board = get_object_or_404(Board, slug=self.kwargs.get('slug'))
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.who_started_topic = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('board_topics', slug=board.slug)
        context = {'board': board, 'form': form}
        return render(request, self.template_name, context)


class ReplyPostView(View):
    template_name = 'forum/reply_post.html'

    def get(self, request, *args, **kwargs):
        form = ReplyPostForm()
        topic = get_object_or_404(Topic,
                                  board__slug=self.kwargs.get('slug'),
                                  slug=self.kwargs.get('topic_slug')
                                  )
        context = {
            'topic': topic,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, board__slug=self.kwargs.get('slug'),
                                  slug=self.kwargs.get('topic_slug')
                                  )
        form = ReplyPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            return redirect('topic_posts', slug=topic.board.slug, topic_slug=topic.slug)
        context = {'topic': topic, 'form': form}
        return render(request, self.template_name, context)
