from django.urls import path
from . import views

app_name = 'asignacion_curso'

urlpatterns = [
    path('', views.AsignacionCursoListView.as_view(), name='list'),
    path('create/', views.AsignacionCursoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.AsignacionCursoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.AsignacionCursoDeleteView.as_view(), name='delete'),
]