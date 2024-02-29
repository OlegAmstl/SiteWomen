from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import AddPostForm
from .models import Women, TagPost
from .utils import DataMixin


class WomenHome(DataMixin, ListView):
    """Отображение главной страницы."""

    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Women.published.all().select_related('cat')


def about(request):
    data = {
        'title': 'About'
    }
    return render(request, 'women/about.html', data)


def categories(request, cat_id):
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>id: {cat_id}</p>')


def categories_by_slug(request, cat_slug):
    return HttpResponse(
        f'<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class AddPage(LoginRequiredMixin,
              PermissionRequiredMixin,
              DataMixin,
              CreateView):
    """Представление добавления поста."""

    form_class = AddPostForm
    template_name = 'women/addpage.html'
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.author
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin,
                 DataMixin, UpdateView):
    """Представление изменения поста."""

    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'


def contact(request):
    return HttpResponse(f'Обратная связь')


def login(request):
    return HttpResponse(f'Авторизация')


class ShowPost(DataMixin, DetailView):
    """Представление о посте."""

    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published,
                                 slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    """Представление категории женщин."""

    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(
            cat__slug=self.kwargs['cat_slug']
        ).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk)


class TagPostList(DataMixin, ListView):
    """Представление тегов."""

    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context,
                                      title='Тег: ' + tag.tag,)

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs['tag_slug']).select_related('cat')
