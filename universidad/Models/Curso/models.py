from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from universidad.Models.catedratico.models import Catedratico

class Curso(models.Model):
    nombre      = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    creditos    = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name="Créditos")
    docente     = models.ForeignKey(
        Catedratico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cursos',
        verbose_name="Docente"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        db_table            = 'curso'
        ordering            = ['nombre']
        verbose_name        = 'Curso'
        verbose_name_plural = 'Cursos'