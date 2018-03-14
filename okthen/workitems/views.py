from django.shortcuts import render,redirect, get_object_or_404
from tasks.forms import ModalTask, DefectoForm
from workitems.forms import WorkItemForm
from okthen.sessions import validate
from proyectos.models import Proyecto
from .models import WorkItem
from django.http import HttpResponse

def ver_workitem(request, id_workitem):
    valid = validate(request)
    if valid == True:
        workitem = get_object_or_404(WorkItem, pk=id_workitem)
        form_task = ModalTask()
        form_defecto = DefectoForm()
        return render(request, 'detalle_work_item.html', {'workitem':workitem,'form_task':form_task, 'form_defecto':form_defecto})
    return valid

def agregar_workitem(request, id_proyecto):
    valid = validate(request)
    if valid == True:
        if request.method == 'POST':
            form = WorkItemForm(request.POST)
            if form.is_valid():
                workitem = form.save(commit=False)
                proyecto =  get_object_or_404(Proyecto, pk=id_proyecto)
                workitem.proyecto = proyecto
                workitem.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return valid

def obtener_tasks_work_item(request):
    workitem = request.GET.get('workitem')
    tasks = WorkItem.objects.get(id=workitem).task_set.all().filter(informacion_defecto__isnull=True)
    response = "<option value="" selected="">---------</option>"
    # Armar opciones
    for task in tasks:
        response += "<option value='" + str(task.id) + "'>" + task.descripcion + "</option>"
    return HttpResponse(response)