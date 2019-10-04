from django.contrib import admin

from .models import Post, Topic, Board

admin.site.register(Post)
admin.site.register(Board)
admin.site.register(Topic)
