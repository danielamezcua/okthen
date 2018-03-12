from django.shortcuts import render
from .forms import AcabarTask

def ver_task(request):
    form_acabar_task = AcabarTask()
    return render(request, 'detalle_task.html', {'form_acabar_task':form_acabar_task})