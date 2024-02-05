from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    """Менеджер для опубликованных постов."""

    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Women(models.Model):

    class Status(models.IntegerChoices):

        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=250,
                             verbose_name='Название')
    slug = models.SlugField(max_length=255,
                            db_index=True,
                            unique=True,
                            default='',
                            verbose_name='Слаг')
    content = models.TextField(blank=True,
                               verbose_name='Контент')
    time_create = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True,
                                       verbose_name='Дата обновления')
    is_published = models.BooleanField(default=Status.PUBLISHED,
                                       choices=tuple(
                                           map(
                                               lambda x: (bool(x[0]), x[1]),
                                               Status.choices)),
                                       verbose_name='Публикация')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT,
                            related_name='posts',
                            verbose_name='Категория')
    tags = models.ManyToManyField('TagPost', blank=True,
                                  related_name='tags',
                                  verbose_name='Тэги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL,
                                   null=True, blank=True, related_name='woman',
                                   verbose_name='Муж')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering = ['-time_create']

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=100, db_index=True,
                            verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True,
                            verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    """Модель тега."""

    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    """Модель мужа."""

    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.name
