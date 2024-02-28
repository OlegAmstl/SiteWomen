from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse, reverse_lazy

from .forms import LoginUserForm, RegisterUserForm


class LoginUser(LoginView):
    """Вход на сайт."""

    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация'
    }


class RegisterUser(CreateView):
    """Регистрация на сайте."""

    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')


# def logout(request):
#     login(request)
#     return HttpResponse(reverse('users:login'))
