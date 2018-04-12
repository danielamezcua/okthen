from django.shortcuts import render,get_object_or_404, redirect,reverse
from .forms import AcabarTask, ModalTask, DefectoForm
from .models import Task, InfoDefecto
from okthen.sessions import validate
from workitems.models import WorkItem
from personas.models import Persona
import datetime


def ver_task(request, id_task):
    valid = validate(request)
    if valid == True:
        task = get_object_or_404(Task, pk=id_task)
        form_defecto = DefectoForm(proyecto=task.work_item.proyecto)
        form_acabar_task = AcabarTask()
        return render(request, 'detalle_task.html', {'task':task,'form_acabar_task':form_acabar_task, 'form_defecto':form_defecto})
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
                    if task.informacion_defecto:
                        task.estado = 3
                        return redirect('workitems:ver_workitem', task.work_item.id)
                    else:
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
        form_defecto = DefectoForm()
        task = get_object_or_404(Task, pk=id_task)
        return render(request, 'calidad_task.html', {'task':task, 'form_defecto':form_defecto})
    return valid

def terminar_task(request,id_task):
    valid = validate(request)
    if valid == True:
        task = get_object_or_404(Task, pk=id_task)
        task.estado = 3
        task.fecha_termino = datetime.datetime.now()
        task.save()
        return redirect(reverse('workitems:ver_workitem', kwargs={'id_workitem':task.work_item.id}))
    return valid

def agregar_defecto(request):
    valid = validate(request)
    if valid == True:
        form = DefectoForm(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            tiempo_estimado = form.cleaned_data['tiempo_estimado']
            workitem = form.cleaned_data['workitem']
            t = Task.objects.create(descripcion=descripcion, tiempo_estimado=tiempo_estimado, work_item=workitem, tipo='DEFECTOS')
            t.save()
            persona = get_object_or_404(Persona, nombre=request.session['user'])
            task_asociado = form.cleaned_data['task']
            tipo = form.cleaned_data['tipo']
            d = InfoDefecto.objects.create(persona=persona, task_asociado=task_asociado, task_encontrado=task_asociado, tipo=tipo)
            d.save()
            t.informacion_defecto = d
            t.save()

    return redirect(request.META.get('HTTP_REFERER'))

def agregar_defecto_encontrado(request,id_task):
    valid = validate(request)
    if valid == True:
        form = DefectoForm(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            tiempo_estimado = form.cleaned_data['tiempo_estimado']
            workitem = form.cleaned_data['workitem']
            t = Task.objects.create(descripcion=descripcion, tiempo_estimado=tiempo_estimado, work_item=workitem, tipo='DEFECTOS')
            t.save()
            persona = get_object_or_404(Persona, nombre=request.session['user'])
            task_asociado = form.cleaned_data['task']
            task_encontrado = get_object_or_404(Task, pk=id_task)
            tipo = form.cleaned_data['tipo']
            d = InfoDefecto.objects.create(persona=persona, task_asociado=task_asociado, task_encontrado=task_encontrado,tipo=tipo)
            d.save()
            t.informacion_defecto = d
            t.save()

    return redirect(request.META.get('HTTP_REFERER'))
