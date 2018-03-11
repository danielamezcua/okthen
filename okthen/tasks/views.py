from django.shortcuts import render

def ver_task(request):
    return render(request, 'detalle_task.html')