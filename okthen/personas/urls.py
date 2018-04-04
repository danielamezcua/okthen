from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'personas'

urlpatterns = [
    path('', views.index, name='index'),
    path('resumen/<int:id_persona>', views.resumen, name='resumen'),
    path('consulta_fases/<int:id_persona>', views.consulta_fases, name='consulta_fases'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
