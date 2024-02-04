from django.contrib import admin
from django.urls import path, include

from women.views import page_not_found

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
]


handler404 = page_not_found
