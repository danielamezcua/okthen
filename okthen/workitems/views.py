from django.shortcuts import render
from tasks.forms import ModalTask

def ver_work_item(request):
    form_task = ModalTask()
    return render(request, 'detalle_work_item.html', {'form_task':form_task})