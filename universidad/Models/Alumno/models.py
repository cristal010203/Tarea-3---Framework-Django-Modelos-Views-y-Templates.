from django.db import models

class Alumno(models.Model):
    first_name   = models.CharField(max_length=100, verbose_name="Nombre")
    last_name    = models.CharField(max_length=100, verbose_name="Apellido")
    email        = models.EmailField(unique=True, verbose_name="Correo electrónico")
    phone        = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    gender       = models.CharField(max_length=1, verbose_name="Género")
    birth_date   = models.DateField(verbose_name="Fecha de nacimiento")
    enrolled_at  = models.DateField(auto_now_add=True, verbose_name="Fecha de inscripción")
    is_active    = models.BooleanField(default=True, verbose_name="Activo")
    carnet       = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Carné",
        null=True,        
        blank=True,
        help_text="Número de carné de 10 dígitos"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.carnet})"

    class Meta:
        db_table            = 'alumno'
        ordering            = ['last_name', 'first_name']
        verbose_name        = 'Alumno'
        verbose_name_plural = 'Alumnos'
        indexes = [ models.Index(fields=['last_name', 'first_name'], name='alumno_nombre_idx'),
                    models.Index(fields=['is_active'],               name='alumno_activo_idx'), 
                    models.Index(fields=['carnet'],                  name='alumno_carnet_idx'),
                    ]