from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class LoginUserForm(AuthenticationForm):
    """Форма для входа на сайт."""

    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               attrs={'class': 'form-input'})
    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
