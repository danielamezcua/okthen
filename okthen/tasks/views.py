from django.shortcuts import render,get_object_or_404, redirect,reverse
from .forms import AcabarTask, ModalTask
from .models import Task
from okthen.sessions import validate
from workitems.models import WorkItem
from personas.models import Persona
import datetime


def ver_task(request, id_task):
    valid = validate(request)
    if valid == True:
        task = get_object_or_404(Task, pk=id_task)
        form_acabar_task = AcabarTask()
        return render(request, 'detalle_task.html', {'task':task,'form_acabar_task':form_acabar_task})
    return valid

def agregar_task(request, id_workitem):
    valid = validate(request)
    if valid == True:
        if request.method == 'POST':
            form = ModalTask(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                workitem = get_object_or_404(WorkItem, pk=id_workitem)
                task.work_item = workitem
                task.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return valid

def log_task(request, id_task):
    valid = validate(request)
    if valid == True:
        if request.method == 'POST':
            task = get_object_or_404(Task, pk=id_task)
            persona = get_object_or_404(Persona, nombre=request.session['user'])
            form = AcabarTask(request.POST)
            if form.is_valid():
                print("hola")
                log = form.save(commit=False)
                tiempo = log.fin-log.inicio
                log.tiempo = tiempo.total_seconds()/3600.0
                #No se acabó
                if form.cleaned_data['acabada'] == 0:
                    if task.estado == 0:
                        task.estado = 1
                #Sí se acabó
                elif form.cleaned_data['acabada'] == 1:
                    task.estado = 2
                task.save()
                log.task = task
                log.persona = persona
                log.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return valid

def calidad_task(request, id_task):
    valid = validate(request)
    if valid == True:
        task = get_object_or_404(Task, pk=id_task)
        return render(request, 'calidad_task.html', {'task':task})
    return valid

def terminar_task(request,id_task):
    valid = validate(request)
    if valid == True:
        task = get_object_or_404(Task, pk=id_task)
        task.estado = 3
        task.save()
        return redirect(reverse('workitems:ver_workitem', kwargs={'id_workitem':task.work_item.id}))
    return valid


