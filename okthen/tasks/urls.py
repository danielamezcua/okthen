from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tasks'

urlpatterns = [
    path('ver_task', views.ver_task, name='ver_task'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
