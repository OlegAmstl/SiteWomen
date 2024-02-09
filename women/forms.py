from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .models import Category, Husband, Women


class AddPostForm(forms.ModelForm):
    """Форма добавления поста."""

    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label='Категория',
                                 empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(),
                                     required=False, label='Муж',
                                     empty_label='Не замужем')

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'is_published',
                  'cat', 'husband', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5})
        }
        labels = {'slug': 'URL'}
