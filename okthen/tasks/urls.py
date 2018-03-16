from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'tasks'

urlpatterns = [
    path('agregar_task/<int:id_workitem>', views.agregar_task, name='agregar_task'),
    path('ver_task/<int:id_task>', views.ver_task, name='ver_task'),
    path('log_task/<int:id_task>', views.log_task, name='log_task'),
    path('calidad_task/<int:id_task>', views.calidad_task, name='calidad_task'),
    path('terminar_task/<int:id_task>', views.terminar_task, name='terminar_task'),
    path('agregar_defecto/', views.agregar_defecto, name='agregar_defecto'),
    path('agregar_defecto/<int:id_task>', views.agregar_defecto_encontrado, name='agregar_defecto_encontrado'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
