from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse

from .models import Women, Category, TagPost
from .forms import AddPostForm

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]


def index(request):
    posts = Women.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'women/index.html', data)


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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat')

    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'women/index.html', data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(
        is_published=Women.Status.PUBLISHED).select_related('cat')

    data = {
        'title': f'Тэг: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None
    }
    return render(request, 'women/index.html', context=data)
