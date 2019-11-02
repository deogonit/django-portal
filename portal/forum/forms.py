from django import forms
from .models import Topic, Post, Board


class NewBoardForm(forms.ModelForm):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Enter description your\'s board'
            }),
        max_length=100,

    )

    class Meta:
        model = Board
        fields = [
            'name',
            'description'
        ]


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'placeholder': 'What is on your mind?'
            }),
        max_length=400,
        help_text='The max length of  the text is 400'
    )
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Topic
        fields = [
            'name',
            'message'
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'message',
        ]
