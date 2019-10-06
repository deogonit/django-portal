from django import forms
from .models import Topic, Post


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'What is on your mind?'
            }),
        max_length=400,
        help_text='The max length of  the text is 400'
    )

    class Meta:
        model = Topic
        fields = [
            'name',
            'message'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }
