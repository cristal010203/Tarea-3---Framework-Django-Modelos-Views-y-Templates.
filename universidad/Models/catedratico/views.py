from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Catedratico

class CatedraticoListView(ListView):
    model = Catedratico
    template_name = 'catedratico/list.html'

class CatedraticoCreateView(CreateView):
    model = Catedratico
    fields = ['nombre', 'especialidad']
    template_name = 'catedratico/form.html'
    success_url = reverse_lazy('catedratico:list')

class CatedraticoUpdateView(UpdateView):
    model = Catedratico
    fields = ['nombre', 'especialidad']
    template_name = 'catedratico/form.html'
    success_url = reverse_lazy('catedratico:list')

class CatedraticoDeleteView(DeleteView):
    model = Catedratico
    template_name = 'catedratico/confirm_delete.html'
    success_url = reverse_lazy('catedratico:list')
