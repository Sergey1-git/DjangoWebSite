from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин")
    password1 = forms.CharField(label="Пароль")
    password2 = forms.CharField(label="Повтор пароля")