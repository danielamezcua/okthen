from django.db import models
from proyectos.models import Proyecto

class WorkItem(models.Model):
    nombre = models.CharField(max_length=400)
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def obtener_tasks_sin_defectos(self):
        return self.task_set.filter(informacion_defecto__isnull=True)

    def obtener_defectos(self):
        return self.task_set.filter(informacion_defecto__isnull=False)
