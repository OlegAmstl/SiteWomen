from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from women.views import page_not_found
from sitewomen import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found

admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Известные женщины мира'
