from django import forms
from django_summernote.widgets import SummernoteWidget

from todolist.models import Todo, Comment
from .models import BlogPost


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '할 일 제목을 입력하세요',
            }),
            'description': SummernoteWidget(attrs={
                'summernote': {'width': '100%', 'height': '300px'}
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'is_completed',
            'completed_image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '할 일 제목을 입력하세요',
            }),
            'description': SummernoteWidget(attrs={
                'summernote': {'width': '100%', 'height': '300px'}
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'is_completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
            'completed_image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message': '내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'class': 'form-control',
                'placeholder': '댓글을 입력해주세요...',
            }),
        }