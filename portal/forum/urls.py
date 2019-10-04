from django.urls import path

from .views import board_view

urlpatterns = [
    path('', board_view, name='boards')
]
