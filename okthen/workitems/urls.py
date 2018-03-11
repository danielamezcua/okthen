from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'workitems'

urlpatterns = [
    path('workitem', views.ver_work_item, name='ver_work_item'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
