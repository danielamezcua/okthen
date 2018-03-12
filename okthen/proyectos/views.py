from django.shortcuts import render,redirect, get_object_or_404
from workitems.forms import WorkItemForm
from .models import Proyecto
from okthen.sessions import validate


def detalle_proyecto(request, id_proyecto):
    valid = validate(request)
    if valid == True:
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
        form_work_item = WorkItemForm()
        return render(request, 'detalle_proyecto.html', {'form_work_item':form_work_item, 'proyecto':proyecto})
    return valid

def index(request):
    valid = validate(request)
    if valid == True:
        proyectos = Proyecto.objects.all()
        return render(request, 'index_proyectos.html', {'proyectos':proyectos})
    return valid

def agregar_proyecto(request):
    valid = validate(request)
    if valid == True:
        validate(request)
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            Proyecto.objects.create(nombre=nombre)
        return redirect(request.META.get('HTTP_REFERER'))
    return valid


