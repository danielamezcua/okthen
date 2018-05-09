from django.shortcuts import render,redirect, get_object_or_404
from workitems.forms import WorkItemForm
from .models import Proyecto
from tasks.models import *
from django.db.models import Sum, Count
from okthen.sessions import validate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db import connection

def detalle_proyecto(request, id_proyecto):
    valid = validate(request)
    if valid == True:
        proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
        workitems = proyecto.workitem_set.all()
        form_work_item = WorkItemForm()
        cursor = connection.cursor()
        #TIEMPO FASES
        cursor.execute(
        '''
        SELECT tipo, SUM(tiempo_estimado) as planeado
        FROM (SELECT tasks_task.id, tipo, tiempo_estimado
        FROM "tasks_task"
        INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
        INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
        INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
        WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
        GROUP BY tipo''',[id_proyecto])
        tiempo_planeado = cursor.fetchall()
        cursor.execute(
        '''
        SELECT tipo, SUM(tiempo) as valor
        FROM (SELECT tasks_task.id, tipo, tiempo
        FROM "tasks_task"
        INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
        INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
        INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
        WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
        GROUP BY tipo''',[id_proyecto])
        tiempo_real = cursor.fetchall()
        tiempos = []
        tiempo_planeado_total = 0
        tiempo_real_total = 0
        for tiempo in tiempo_planeado:
            for registro in tiempo_real:
                if tiempo[0] == registro[0]:
                    tiempo_planeado_total+=tiempo[1]
                    tiempo_real_total+=registro[1]
                    try:
                        porcentaje = round(((registro[1] * 100) / tiempo[1]),2)
                    except ZeroDivisionError:
                        porcentaje = 0
                    tiempos.append({'tipo':tiempo[0],'planeado':tiempo[1],'real':registro[1],'porcentaje':porcentaje})
        try:
            porcentaje_total = round(tiempo_real_total * 100 / tiempo_planeado_total,2)
        except ZeroDivisionError:
            porcentaje_total = 0
        total = {'tipo':'TOTAL','planeado':tiempo_planeado_total,'real':tiempo_real_total,'porcentaje':porcentaje_total }


        # #DEFECTOS
        defectos_inyectados = Task.objects.filter(work_item__proyecto__id=id_proyecto, informacion_defecto__isnull=False).values('informacion_defecto__task_asociado__tipo').annotate(task_asociado__tipo__count=Count('informacion_defecto__task_asociado__tipo')).exclude(informacion_defecto__task_asociado__tipo__isnull=True)
        defectos_resueltos = Task.objects.values('informacion_defecto__task_asociado__tipo').filter(work_item__proyecto__id=id_proyecto).filter(estado=3).annotate(Count('informacion_defecto__task_asociado__tipo')).exclude(informacion_defecto__task_asociado__tipo=None)
        defectos = []
        total_inyectados = 0
        total_resueltos = 0
        for x in defectos_inyectados:
                for z in defectos_resueltos:
                    if x['informacion_defecto__task_asociado__tipo'] == z['informacion_defecto__task_asociado__tipo']:
                        total_inyectados+=x['task_asociado__tipo__count']
                        total_resueltos+=z['informacion_defecto__task_asociado__tipo__count']
                        try:
                            porcentaje = round(((z['informacion_defecto__task_asociado__tipo__count'] * 100) / x['task_asociado__tipo__count']),2)
                        except ZeroDivisionError:
                            porcentaje = 0
                        defectos.append({'tipo':x['informacion_defecto__task_asociado__tipo'],'inyectados':x['task_asociado__tipo__count'],'resueltos':z['informacion_defecto__task_asociado__tipo__count'],'porcentaje':porcentaje})

        cantidad_a_sumar_inyectados = 0
        cantidad_a_sumar_resueltos = 0
        for defecto in defectos:
            if defecto['tipo'] == "DEFECTOS":
                cantidad_a_sumar_inyectados = defecto['inyectados']
                cantidad_a_sumar_resueltos = defecto['resueltos']
                defectos.remove(defecto)

        for defecto in defectos:
            if defecto['tipo'] == "DESARROLLO":
                defecto['inyectados'] += cantidad_a_sumar_inyectados
                defecto['resueltos'] += cantidad_a_sumar_resueltos
                try:
                    porcentaje = round(defecto['resueltos']*100/defecto['inyectados'],2)
                except ZeroDivisionError:
                    porcentaje = 0
                defecto['porcentaje'] = porcentaje


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
            cursor = connection.cursor()
            #TIEMPO FASES
            cursor.execute(
            '''
            SELECT tipo, SUM(tiempo_estimado) as planeado
            FROM (SELECT tasks_task.id, tipo, tiempo_estimado
            FROM "tasks_task"
            INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
            INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
            INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
            WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
            GROUP BY tipo''',[id_proyecto])
            tiempo_planeado = cursor.fetchall()
            cursor.execute(
            '''
            SELECT tipo, SUM(tiempo) as valor
            FROM (SELECT tasks_task.id, tipo, tiempo
            FROM "tasks_task"
            INNER JOIN "tasks_personataskrelacion" ON ("tasks_task"."id" = "tasks_personataskrelacion"."task_id")
            INNER JOIN "personas_persona" ON ("tasks_personataskrelacion"."persona_id" = "personas_persona"."id")
            INNER JOIN "workitems_workitem" ON ("tasks_task"."work_item_id" = "workitems_workitem"."id")
            WHERE ("workitems_workitem"."proyecto_id" = %s AND NOT ("tasks_task"."tipo" IS NULL))) as sub
            GROUP BY tipo''',[id_proyecto])
            tiempo_real = cursor.fetchall()
            data_planeado = []
            data_real = []
            fases = []
            for tiempo in tiempo_planeado:
                data_planeado.append(float(tiempo[1]))
                fases.append(tiempo[0])
            valores.append({'label':'Planeado','backgroundColor':'gray','data':data_planeado})
            for tiempo in tiempo_real:
                data_real.append(float(tiempo[1]))
            valores.append({'label':'Real','backgroundColor':'black','data':data_real})
            data = {
                "labels":fases,
                "datasets":valores
            }
            return JsonResponse(data)

def consulta_defectos(request, id_proyecto):
    if request.method == 'POST':
            valores = []
            numeros = Task.objects.filter(work_item__proyecto__id=id_proyecto, informacion_defecto__isnull=False).values('informacion_defecto__fecha').annotate(Count('informacion_defecto__fecha')).order_by('informacion_defecto__fecha')
            numeros_hechos = Task.objects.values('fecha_termino').exclude(informacion_defecto_id=None).filter(work_item__proyecto__id=id_proyecto).filter(estado=3).annotate(Count('fecha_termino')).order_by('fecha_termino')
            data_defectos = []
            data_defectos_hechos = []
            fechas = []
            for numero in numeros:
                fechas.append(numero['informacion_defecto__fecha'])

            for numero in numeros_hechos:
                if numero['fecha_termino'] not in fechas:
                    fechas.append(numero['fecha_termino'])
            fechas.sort()
            i = 0
            j = 0
            for fecha in fechas:
                try:
                    if fecha == numeros[i]['informacion_defecto__fecha']:
                        data_defectos.append(numeros[i]['informacion_defecto__fecha__count'])
                        i = i + 1
                    else:
                        data_defectos.append(0)
                except IndexError:
                    data_defectos.append(0)

                try:
                    if fecha == numeros_hechos[j]['fecha_termino']:
                        data_defectos_hechos.append(numeros_hechos[j]['fecha_termino__count'])
                        j = j + 1
                    else:
                        data_defectos_hechos.append(0)
                except IndexError:
                    data_defectos_hechos.append(0)

            valores = []
            valores.append({'label':'Defectos encontrados','borderColor':'red','data':data_defectos,'fill':False})
            valores.append({'label':'Defectos arreglados','borderColor':'blue','data':data_defectos_hechos,'fill':False})
            data = {
                "labels":fechas,
                "datasets":valores
            }
            return JsonResponse(data)
