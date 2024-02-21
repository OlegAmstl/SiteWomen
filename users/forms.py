from django import forms


class LoginUserForm(forms.Form):
    """Форма для входа на сайт."""

    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль',
                               attrs={'class': 'form-input'})
