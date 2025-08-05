from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '이름을 입력하세요',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '이메일 주소',
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '비밀번호 확인',
            }),
        }

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '이메일 주소',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '비밀번호',
    }))
