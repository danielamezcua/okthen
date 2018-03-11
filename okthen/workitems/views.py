from django.shortcuts import render


def ver_work_item(request):
    return render(request, 'detalle_work_item.html')