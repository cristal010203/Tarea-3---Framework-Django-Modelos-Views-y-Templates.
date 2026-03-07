from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import InscripcionAlumno

class InscripcionAlumnoListView(ListView):
    model = InscripcionAlumno
    template_name = 'inscripcion_alumno/list.html'

class InscripcionAlumnoCreateView(CreateView):
    model = InscripcionAlumno
    fields = ['alumno', 'asignacion_curso']
    template_name = 'inscripcion_alumno/form.html'
    success_url = reverse_lazy('inscripcion_alumno:list')

class InscripcionAlumnoUpdateView(UpdateView):
    model = InscripcionAlumno
    fields = ['alumno', 'asignacion_curso']
    template_name = 'inscripcion_alumno/form.html'
    success_url = reverse_lazy('inscripcion_alumno:list')

class InscripcionAlumnoDeleteView(DeleteView):
    model = InscripcionAlumno
    template_name = 'inscripcion_alumno/confirm_delete.html'
    success_url = reverse_lazy('inscripcion_alumno:list')
