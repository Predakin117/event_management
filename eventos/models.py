from django.db import models


class Evento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField()
    lugar = models.CharField(max_length=200)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return self.nombre
