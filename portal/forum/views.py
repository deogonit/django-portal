from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm


class BoardView(View):
    template_name = 'forum/boards.html'

    def get(self, request, *args, **kwargs):
        boards = Board.objects.all()
        context = {
            'boards': boards
        }
        return render(request, self.template_name, context)


def create_page(request, objects, count_of_pages):
    paginator = Paginator(objects, count_of_pages)
    page_number = request.GET.get('page', 1)
    return paginator.get_page(page_number)


class BoardTopicsView(View):
    template_name = 'forum/board_topics.html'

    def get(self, request, slug):
        board = get_object_or_404(Board, slug__iexact=slug)
        topics = Topic.objects.filter(board=board)
        topics = create_page(request, topics, 2)

        context = {
            'board': board,
            'page_objects': topics
        }
        return render(request, self.template_name, context)


# TODO: 3. For posts.html make a version for mobile (adaptive design)
# TODO: 8. Make deleting posts for all users (topics and boards for admins or moderator)


class TopicPostsView(View):
    template_name = 'forum/topic_posts.html'

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic,
                                  board__slug=self.kwargs.get('slug'),
                                  slug=self.kwargs.get('topic_slug')
                                  )
        topic.views += 1
        topic.save()
        posts = Post.objects.filter(topic=topic)
        posts = create_page(request, posts, 3)
        context = {
            'topic': topic,
            'page_objects': posts
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ReplyPostView(View):
    template_name = 'forum/reply_post.html'

    def get(self, request, *args, **kwargs):
        form = PostForm()
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'))
        context = {
            'topic': topic,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'))
        form = PostForm(request.POST)
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


@method_decorator(login_required, name='dispatch')
class EditPostView(View):
    template_name = 'forum/edit_post.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_number'))
        bound_form = PostForm(instance=post)
        context = {
            'form': bound_form,
            'post': post
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs.get('post_number'))
        topic = Topic.objects.get(slug=self.kwargs.get('topic_slug'))
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = timezone.now()
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            return redirect('topic_posts', slug=topic.board.slug, topic_slug=topic.slug)
        context = {'post': post, 'form': form}
        return render(request, self.template_name, context)
