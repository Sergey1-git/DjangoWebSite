from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from .forms import RegisterUserForm


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}


    def get_success_url(self):
        return reverse_lazy('home')



class RegisterUser(CreateView):
    form_class=RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
