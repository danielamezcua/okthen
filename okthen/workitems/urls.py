from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'workitems'

urlpatterns = [
    path('ver_workitem/<int:id_workitem>', views.ver_workitem, name='ver_workitem'),
    path('agregar_workitem/<int:id_proyecto>', views.agregar_workitem, name='agregar_workitem'),
    path('obtener_tasks_work_item', views.obtener_tasks_work_item, name='obtener_tasks_work_item'),
    path('elimina_task/<int:id_workitem>/<int:id_task>', views.elimina_task, name='elimina_task'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
