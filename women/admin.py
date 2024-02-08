from django.contrib import admin

from .models import Women, Category


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ['title', 'time_create', 'is_published', 'cat', 'brif_info']
    list_display_links = ['title']
    ordering = ['time_create', 'title']
    list_editable = ('is_published',)
    list_per_page = 5

    @admin.display(description='Краткое описание')
    def brif_info(self, women: Women):
        return f'Описание {len(women.content)} символов.'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
