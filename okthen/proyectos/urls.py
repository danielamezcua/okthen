from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'proyectos'

urlpatterns = [
    path('ver_proyecto', views.ver_proyecto, name='ver_proyecto'),
    path('agregar_proyecto', views.agregar_proyecto, name='agregar_proyecto'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
