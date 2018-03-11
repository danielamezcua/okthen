from django.shortcuts import render


def ver_proyecto(request):
    return render(request, 'detalle_proyecto.html')