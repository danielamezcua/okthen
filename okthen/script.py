from tasks.models import *
from proyectos.models import *
TIPOS = {1:"PLAN", 2:'DISEÑO', 3:'DESARROLLO', 4:'PRUEBAS', 5:'POSTMORTEM', 6:'DEFECTOS'}

#A los tasks que tengan información de defectos y que no tengan el tipo DEFECTOS, se le asigna este tipo
def asignar_tipo_defectos_a_defectos(id_proyecto):
    proyecto = Proyecto.objects.get(id=id_proyecto)
    print("Proyecto: " + str(proyecto.nombre.encode('utf-8')))
    print("Obteniendo defectos sin un tipo...")
    defectos_sin_tipo = Task.objects.filter(work_item__proyecto__id=id_proyecto, informacion_defecto__isnull=False, tipo__isnull=True)
    print('Numeros de defectos sin tipo: ' + str(defectos_sin_tipo.count()))
    print("Asignando tipo DEFECTOS...")
    for defecto_sin_tipo in defectos_sin_tipo:
        defecto_sin_tipo.tipo = "DEFECTOS"
        defecto_sin_tipo.save()
    print("Listo")

def asignar_tipo_a_faltantes(id_proyecto):
    tasks_sin_tipo = Task.objects.filter(work_item__proyecto__id=id_proyecto, tipo__isnull=True)
    for task_sin_tipo in tasks_sin_tipo:
        print(str(task_sin_tipo.work_item).encode('utf-8'))
        print(str(task_sin_tipo).encode('utf-8'))
        tipo = input("1. PLAN | 2. DISENO | 3. DESARROLLO | 4. PRUEBAS | 5 POSTMORTEM | 6. DEFECTOS: ")
        task_sin_tipo.tipo = TIPOS[int(tipo)]
        task_sin_tipo.save()
        print("----------------")
