from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
import json
from .models import Board, Topic, Post, LikeDislike
from .forms import NewTopicForm, PostForm, NewBoardForm, EditTopicForm
from .decorators import moderator_required, administrator_required


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
        topics = create_page(request, topics, 5)

        context = {
            'board': board,
            'page_objects': topics
        }
        return render(request, self.template_name, context)


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
        posts = create_page(request, posts, 10)
        context = {
            'topic': topic,
            'page_objects': posts
        }
        return render(request, self.template_name, context)


@method_decorator([login_required, moderator_required, administrator_required], name='dispatch')
class NewBoardView(View):
    template_name = 'forum/new_board.html'

    def get(self, request, *args, **kwargs):
        form = NewBoardForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = NewBoardForm(request.POST)
        if form.is_valid():
            board = form.save()
            return redirect('boards')
        context = {'form': form}
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


class VotesView(View):
    model = None
    vote_type = None

    def post(self, request, *args, **kwargs):
        obj_pk = self.kwargs.get('post_number')
        obj = self.model.objects.get(pk=obj_pk)
        try:
            likedislike = LikeDislike.objects.get(content_type=ContentType.objects.get_for_model(obj), object_id=obj.pk,
                                                  user=request.user)

            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(user=request.user, vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating(),
                'post_number': obj_pk
            }),
            content_type="application/json"
        )


@method_decorator(login_required, name='dispatch')
class DeletePostView(View):
    template_name = 'forum/delete_post.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_number'))
        context = {'post': post}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs.get('post_number'))
        topic = post.topic
        if topic.posts.count() == 1:
            post.delete()
            topic.delete()
            return redirect('board_topics', slug=topic.board.slug)
        post.delete()
        return redirect('topic_posts', slug=post.topic.board.slug, topic_slug=post.topic.slug)


@method_decorator([login_required, moderator_required, administrator_required], name='dispatch')
class EditTopicView(View):
    template_name = 'forum/edit_topic.html'

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'))
        bound_form = EditTopicForm(instance=topic)
        context = {
            'topic': topic,
            'form': bound_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        topic = Topic.objects.get(slug=self.kwargs.get('topic_slug'))
        form = EditTopicForm(request.POST, instance=topic)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.save()
            return redirect('topic_posts', slug=topic.board.slug, topic_slug=topic.slug)
        context = {'topic': topic, 'form': form}
        return render(request, self.template_name, context)


@method_decorator([login_required, moderator_required, administrator_required ], name='dispatch')
class DeleteTopicView(View):
    template_name = 'forum/delete_topic.html'

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic, slug=self.kwargs.get('topic_slug'))
        context = {
            'topic': topic,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        topic = Topic.objects.get(slug=self.kwargs.get('topic_slug'))
        topic.delete()
        return redirect('board_topics', slug=topic.board.slug)
