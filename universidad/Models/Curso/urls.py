from django.urls import path
from . import views

app_name = 'curso'

urlpatterns = [
    path('', views.CursoListView.as_view(), name='list'),
    path('create/', views.CursoCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.CursoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.CursoDeleteView.as_view(), name='delete'),
]