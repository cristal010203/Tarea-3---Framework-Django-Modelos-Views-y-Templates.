from django.db import models
from django.core.exceptions import ValidationError
from universidad.Models.Curso.models import Curso
from universidad.Models.Alumno.models import Alumno


class AsignacionCurso(models.Model):
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name="Curso"
    )
    catedratico = models.ForeignKey(
        'catedratico.Catedratico',  # app_label.ModelName
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='asignaciones',
        verbose_name="Catedrático"
    )
    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='asignaciones',
        verbose_name="Alumno",
        limit_choices_to={'is_active': True}
    )
    horario = models.CharField(max_length=100, verbose_name="Horario")
    aula    = models.CharField(max_length=50, verbose_name="Aula")
    cupo    = models.PositiveIntegerField(verbose_name="Cupo máximo")

    def clean(self):
        if self.curso_id and self.curso.docente:
            self.catedratico = self.curso.docente

        if self.alumno_id and not self.alumno.is_active:
            raise ValidationError({
                'alumno': 'Solo se pueden asignar alumnos activos.'
            })

        if self.alumno_id and self.curso_id:
            existe = AsignacionCurso.objects.filter(
                curso=self.curso,
                alumno=self.alumno
            ).exclude(pk=self.pk).exists()
            if existe:
                raise ValidationError({
                    'alumno': 'Este alumno ya está asignado a este curso.'
                })

    def save(self, *args, **kwargs):
        if self.curso_id and self.curso.docente:
            self.catedratico = self.curso.docente
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno.carnet} — {self.curso.nombre}"

    class Meta:
        db_table            = 'asignacion_curso'
        ordering            = ['curso', 'alumno']
        verbose_name        = 'Asignación de Curso'
        verbose_name_plural = 'Asignaciones de Cursos'
        unique_together     = [('curso', 'alumno')]
        indexes = [
    models.Index(fields=['alumno'],      name='asig_alumno_idx'),
    models.Index(fields=['catedratico'], name='asig_catedratico_idx'),
    models.Index(fields=['curso'],       name='asig_curso_idx'),
    ]