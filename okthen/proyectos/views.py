from django.shortcuts import render,redirect, get_object_or_404
from workitems.forms import WorkItemForm
from .models import Proyecto
from tasks.models import *
from django.db.models import Sum, Count
from okthen.sessions import validate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse


def detalle_proyecto(request, id_proyecto):
    valid = validate(request)
    if valid == True:
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
        workitems = proyecto.workitem_set.all()
        form_work_item = WorkItemForm()
        #TIEMPO FASES
        tiempo_planeado = Task.objects.raw(
        '''
        SELECT id ,tipo, SUM(tiempo_estimado) as planeado
        FROM (SELECT DISTINCT tasks_task.id, tipo, tiempo_estimado
        FROM "tasks_task"
        INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
        INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
        INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
        WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
        GROUP BY tipo,id''',[id_proyecto])
        tiempo_real = Task.objects.raw(
        '''
        SELECT id ,tipo, SUM(tiempo) as valor
        FROM (SELECT DISTINCT tasks_task.id, tipo, tiempo
        FROM "tasks_task"
        INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
        INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
        INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
        WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
        GROUP BY tipo,id''',[id_proyecto])
        tiempos = []
        tiempo_planeado_total = 0
        tiempo_real_total = 0
        for tiempo in tiempo_planeado:
            for registro in tiempo_real:
                if tiempo.tipo == registro.tipo:
                    tiempo_planeado_total+=tiempo.planeado
                    tiempo_real_total+=registro.valor
                    try:
                        porcentaje = round(((registro.valor * 100) / tiempo.planeado),2)
                    except ZeroDivisionError:
                        porcentaje = 0
                    tiempos.append({'tipo':tiempo.tipo,'planeado':tiempo.planeado,'real':registro.valor,'porcentaje':porcentaje})
        try:
            porcentaje_total = round(tiempo_real_total * 100 / tiempo_planeado_total,2)
        except ZeroDivisionError:
            porcentaje_total = 0
        total = {'tipo':'TOTAL','planeado':tiempo_planeado_total,'real':tiempo_real_total,'porcentaje':porcentaje_total }
        #DEFECTOS
        defectos_inyectados = InfoDefecto.objects.values('task_asociado__tipo').filter(task_asociado__work_item__proyecto__id=id_proyecto).annotate(Count('task_asociado__tipo'))
        defectos_resueltos = Task.objects.values('informacion_defecto__task_asociado__tipo').filter(work_item__proyecto__id=id_proyecto).filter(estado=3).annotate(Count('informacion_defecto__task_asociado__tipo'))
        defectos = []
        total_inyectados = 0
        total_resueltos = 0
        for x in defectos_inyectados:
                for z in defectos_resueltos:
                    if x['task_asociado__tipo'] == z['informacion_defecto__task_asociado__tipo']:
                        total_inyectados+=x['task_asociado__tipo__count']
                        total_resueltos+=z['informacion_defecto__task_asociado__tipo__count']
                        try:
                            porcentaje = round(((z['informacion_defecto__task_asociado__tipo__count'] * 100) / x['task_asociado__tipo__count']),2)
                        except ZeroDivisionError:
                            porcentaje = 0
                        defectos.append({'tipo':x['task_asociado__tipo'],'inyectados':x['task_asociado__tipo__count'],'resueltos':z['informacion_defecto__task_asociado__tipo__count'],'porcentaje':porcentaje})
        try:
            porcentaje_total = round(((total_resueltos * 100) / total_inyectados),2)
        except ZeroDivisionError:
            porcentaje_total = 0
        total_defectos = {'tipo':'TOTAL','inyectados':total_inyectados,'resueltos':total_resueltos,'porcentaje':porcentaje_total }
        return render(request, 'detalle_proyecto.html', {'form_work_item':form_work_item, 'proyecto':proyecto, 'workitems':workitems,'tiempos':tiempos,'total':total,'defectos':defectos,'total_defectos':total_defectos})
    return valid

def index(request):
    valid = validate(request)
    if valid == True:
        proyectos = Proyecto.objects.all()
        return render(request, 'index_proyectos.html', {'proyectos':proyectos})
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

def consulta_fases(request, id_proyecto):
    if request.method == 'POST':
            valores = []
            tiempo_planeado = Task.objects.raw(
            '''
            SELECT id ,tipo, SUM(tiempo_estimado) as planeado
            FROM (SELECT DISTINCT tasks_task.id, tipo, tiempo_estimado
            FROM "tasks_task"
            INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
            INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
            INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
            WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
            GROUP BY tipo,id''',[id_proyecto])
            tiempo_real = Task.objects.raw(
            '''
            SELECT id ,tipo, SUM(tiempo) as valor
            FROM (SELECT DISTINCT tasks_task.id, tipo, tiempo
            FROM "tasks_task"
            INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
            INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
            INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
            WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
            GROUP BY tipo,id''',[id_proyecto])
            data_planeado = []
            data_real = []
            fases = []
            for tiempo in tiempo_planeado:
                data_planeado.append(float(tiempo.planeado))
                fases.append(tiempo.tipo)
            valores.append({'label':'Planeado','backgroundColor':'gray','data':data_planeado})
            for tiempo in tiempo_real:
                data_real.append(float(tiempo.valor))
            valores.append({'label':'Real','backgroundColor':'black','data':data_real})
            data = {
                "labels":fases,
                "datasets":valores
            }
            return JsonResponse(data)

def consulta_defectos(request, id_proyecto):
    if request.method == 'POST':
            valores = []
            numeros = InfoDefecto.objects.values('fecha').filter(task_asociado__work_item__proyecto__id=id_proyecto).annotate(Count('fecha'))
            data_defectos = []
            fechas = []
            for numero in numeros:
                data_defectos.append(numero['fecha__count'])
                fechas.append(numero['fecha'].strftime('%d/%m/%Y'))
            valores = []
            valores.append({'label':'Defectos por día','borderColor':'gray','data':data_defectos,'fill':False})
            data = {
                "labels":fechas,
                "datasets":valores
            }
            return JsonResponse(data)
