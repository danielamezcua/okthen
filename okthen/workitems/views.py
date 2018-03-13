from django.shortcuts import render,redirect, get_object_or_404
from tasks.forms import ModalTask
from workitems.forms import WorkItemForm
from okthen.sessions import validate
from proyectos.models import Proyecto
from .models import WorkItem

def ver_workitem(request, id_workitem):
    valid = validate(request)
    if valid == True:
        workitem = get_object_or_404(WorkItem, pk=id_workitem)
        form_task = ModalTask()
        return render(request, 'detalle_work_item.html', {'workitem':workitem,'form_task':form_task})
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