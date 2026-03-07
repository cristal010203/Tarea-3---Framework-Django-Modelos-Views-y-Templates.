from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Nota

class NotaListView(ListView):
    model = Nota
    template_name = 'notas/list.html'

class NotaCreateView(CreateView):
    model = Nota
    fields = ['alumno', 'curso', 'nota']
    template_name = 'notas/form.html'
    success_url = reverse_lazy('notas:list')

class NotaUpdateView(UpdateView):
    model = Nota
    fields = ['alumno', 'curso', 'nota']
    template_name = 'notas/form.html'
    success_url = reverse_lazy('notas:list')

class NotaDeleteView(DeleteView):
    model = Nota
    template_name = 'notas/confirm_delete.html'
    success_url = reverse_lazy('notas:list')
