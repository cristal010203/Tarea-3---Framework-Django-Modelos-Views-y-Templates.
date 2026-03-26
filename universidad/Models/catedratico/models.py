from django.db import models

class Catedratico(models.Model):
    first_name   = models.CharField(max_length=100, verbose_name="Nombre")
    last_name    = models.CharField(max_length=100, verbose_name="Apellido")
    especialidad = models.CharField(max_length=100, blank=True, verbose_name="Especialidad")
    email        = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone        = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table  = 'catedratico'
        ordering  = ['last_name', 'first_name']
        verbose_name        = 'Catedrático'
        verbose_name_plural = 'Catedráticos'