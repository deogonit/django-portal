from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.db.models.signals import pre_save
from portal.utils import unique_slug_generator
from django.urls import reverse


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('board_topics', kwargs={'slug': self.slug})

    def get_number_of_topics(self):
        board = Board.objects.get(slug=self.slug)
        return len(board.topics.all())

    def has_board_topics(self):
        number = self.get_number_of_topics()
        return True if number else False


class Topic(models.Model):
    name = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name="topics", on_delete=models.CASCADE)
    who_started_topic = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('topic_posts', kwargs={'slug': self.board.slug, 'topic_slug': self.slug})

    def get_number_replies(self):
        if self.posts.count() > 0:
            return self.posts.count() - 1
        return 0


def pre_save_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.name, instance.slug)


pre_save.connect(pre_save_slug, sender=Board)
pre_save.connect(pre_save_slug, sender=Topic)


class Post(models.Model):
    message = models.TextField(max_length=400)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(15)

    def get_edit_url(self):
        return reverse('edit_post',
                       kwargs={'slug': self.topic.board.slug, 'topic_slug': self.topic.slug, 'post_number': self.pk})

# TODO: 10. Add roles or permutation for group user
# TODO: 11. Add Likes for posts and in future for news
# TODO: 12. Add Comments system for news
