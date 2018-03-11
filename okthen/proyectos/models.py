from django.db import models

class Proyecto(models.Model):
    nombre = models.CharField(blank=False, null=True, max_length=300)

    def __str__(self):
        return self.nombre