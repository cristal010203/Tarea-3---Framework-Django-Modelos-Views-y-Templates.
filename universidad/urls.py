"""
URL configuration for universidad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include

from django import core
from django.contrib import admin
from django.urls import path, include

from core import views as core_views, views

urlpatterns = [
path('', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('alumnos/', include('universidad.Models.Alumno.urls')),
    path('curso/', include('universidad.Models.Curso.urls')),
    path('catedratico/', include('universidad.Models.catedratico.urls')),
    path('notas/', include('universidad.Models.Notas.urls')),
    path('asignacion_curso/', include('universidad.Models.asignacion_curso.urls')),
    path('inscripcion_alumno/', include('universidad.Models.Inscripcion_alumno.urls')),
    path('reportes/', include('universidad.Models.reportes.urls'))
]
