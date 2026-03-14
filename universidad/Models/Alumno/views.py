from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Alumno
from .forms import AlumnoForm
from django.db.models import Q

def alumno_list(request):
    query   = request.GET.get('q', '')
    alumnos = Alumno.objects.all()

    if query:
        alumnos = alumnos.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(email__icontains=query)
    )
    return render(request, 'alumno/list.html', {
        'alumnos': alumnos,
        'query':   query
    })

def alumno_detail(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    return render(request, 'alumno/detail.html', {'alumno': alumno})

def alumno_create(request):
    form = AlumnoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Alumno registrado correctamente.')
        return redirect('alumno:list')
    return render(request, 'alumno/form.html', {
        'form':  form,
        'title': 'Nuevo Alumno'
    })

def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    form   = AlumnoForm(request.POST or None, instance=alumno)
    if form.is_valid():
        form.save()
        messages.success(request, 'Alumno actualizado correctamente.')
        return redirect('alumno:list')
    return render(request, 'alumno/form.html', {
        'form':  form,
        'title': f'Editar: {alumno.first_name} {alumno.last_name}'
    })

def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, 'Alumno eliminado.')
        return redirect('alumno:list')
    return render(request, 'alumno/confirm_delete.html', {'alumno': alumno})