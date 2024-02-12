from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from django.views.generic import ListView, DetailView

from .models import Women, Category, TagPost
from .forms import AddPostForm

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

class WomenHome(ListView):
    """Отображение главной страницы."""

    # model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

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


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    data = {'menu': menu,
            'title': 'Добавить статью',
            'form': form}
    return render(request, 'women/addpage.html', context=data)


def contact(request):
    return HttpResponse(f'Обратная связь')


def login(request):
    return HttpResponse(f'Авторизация')


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1
    }
    return render(request, 'women/post.html', data)


class ShowPost(DetailView):
    """Представление о посте."""

    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = context['post'].title
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published,
                                 slug=self.kwargs[self.slug_url_kwarg])

class WomenCategory(ListView):
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
        context['title'] = 'Категория - ' + str(cat.id)
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context


class TagPostList(ListView):
    """Представление тегов."""

    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(
            tags__slug=self.kwargs['tag_slug']).select_related('cat')
