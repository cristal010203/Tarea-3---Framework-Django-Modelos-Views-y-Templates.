
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Curso

class CursoListView(ListView):
    model = Curso
    template_name = 'curso/list.html'

class CursoCreateView(CreateView):
    model = Curso
    fields = ['nombre', 'descripcion']
    template_name = 'curso/form.html'
    success_url = reverse_lazy('curso:list')

class CursoUpdateView(UpdateView):
    model = Curso
    fields = ['nombre', 'descripcion']
    template_name = 'curso/form.html'
    success_url = reverse_lazy('curso:list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso/confirm_delete.html'
    success_url = reverse_lazy('curso:list')

