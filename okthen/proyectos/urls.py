from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'proyectos'

urlpatterns = [
    path('', views.index, name='index'),
    path('detalle_proyecto/<int:id_proyecto>', views.detalle_proyecto, name='detalle_proyecto'),
    path('agregar_proyecto', views.agregar_proyecto, name='agregar_proyecto'),
    path('consulta_fases/<int:id_proyecto>', views.consulta_fases, name='consulta_fases'),
    path('consulta_defectos/<int:id_proyecto>', views.consulta_defectos, name='consulta_defectos'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
