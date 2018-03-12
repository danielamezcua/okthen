from django.shortcuts import render,redirect
from workitems.forms import WorkItemForm
from .models import Proyecto
from okthen.sessions import validate


def ver_proyecto(request):
    valid = validate(request)
    if valid == True:
        form_work_item = WorkItemForm()
        return render(request, 'detalle_proyecto.html', {'form_work_item':form_work_item})
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


