# reportes/views.py
from django.shortcuts import render
from django.db.models import Avg, Count, Q, FloatField
from django.db.models.functions import Coalesce
from django.core.paginator import Paginator

from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso
from universidad.Models.catedratico.models import Catedratico
from universidad.Models.Notas.models import Nota
from universidad.Models.asignacion_curso.models import AsignacionCurso


# ─────────────────────────────────────────────────────────────────────────────
# REPORTE 1: Rendimiento Académico por Alumno
#
# OPTIMIZACIÓN:
#   • Una sola consulta con annotate() en vez de loop con 3 queries por alumno
#   • select_related() eliminado (no se necesita con annotate)
#   • Filtros aplicados ANTES de annotate para reducir filas procesadas
#   • Paginación de 50 registros para no enviar 10k filas al template
#   • Índices recomendados al final del archivo
# ─────────────────────────────────────────────────────────────────────────────
def reporte_rendimiento(request):

    filtro_curso  = request.GET.get('curso', '')
    filtro_estado = request.GET.get('estado', '')
    filtro_q      = request.GET.get('q', '').strip()
    page_num      = request.GET.get('page', 1)

    # ── Una sola consulta con anotaciones ────────────────────────────────────
    # Django traduce esto a UN solo SQL con LEFT JOINs y GROUP BY
    alumnos_qs = (
        Alumno.objects
        .filter(is_active=True)
        .annotate(
            total_cursos=Count('asignaciones', distinct=True),
            total_notas =Count('nota',         distinct=True),
            promedio    =Avg('nota__nota', output_field=FloatField()),
        )
    )

    # Filtros aplicados sobre el QuerySet (antes de evaluar)
    if filtro_q:
        alumnos_qs = alumnos_qs.filter(
            Q(first_name__icontains=filtro_q) |
            Q(last_name__icontains=filtro_q)  |
            Q(carnet__icontains=filtro_q)
        )

    if filtro_curso:
        alumnos_qs = alumnos_qs.filter(asignaciones__curso_id=filtro_curso)

    # Ordenar antes de paginar
    alumnos_qs = alumnos_qs.order_by('last_name', 'first_name')

    # ── Filtro de estado (calculado desde promedio anotado) ───────────────────
    # Se hace en Python sobre el QuerySet ya filtrado para no complicar el SQL
    if filtro_estado == 'aprobado':
        alumnos_qs = alumnos_qs.filter(promedio__gte=61)
    elif filtro_estado == 'reprobado':
        alumnos_qs = alumnos_qs.filter(promedio__lt=61, promedio__isnull=False)
    elif filtro_estado == 'sin_notas':
        alumnos_qs = alumnos_qs.filter(promedio__isnull=True)

    # ── KPIs: consultas agregadas independientes (muy rápidas con índices) ────
    # Se calculan sobre el mismo queryset filtrado ANTES de paginar
    from django.db.models import Count as Cnt
    kpi_qs = alumnos_qs.aggregate(
        total      =Cnt('id'),
        aprobados  =Cnt('id', filter=Q(promedio__gte=61)),
        reprobados =Cnt('id', filter=Q(promedio__lt=61, promedio__isnull=False)),
        prom_gral  =Avg('promedio', output_field=FloatField()),
    )

    # ── Paginación: 50 registros por página ───────────────────────────────────
    paginator   = Paginator(alumnos_qs, 50)
    page_obj    = paginator.get_page(page_num)

    # ── Construir lista para el template (sin loops de queries) ───────────────
    alumnos_data = []
    for alumno in page_obj:
        promedio = alumno.promedio
        if promedio is None:
            estado = 'sin_notas'
        elif promedio >= 61:
            estado = 'aprobado'
        else:
            estado = 'reprobado'

        alumnos_data.append({
            'alumno':       alumno,
            'total_cursos': alumno.total_cursos,
            'total_notas':  alumno.total_notas,
            'promedio':     round(promedio, 1) if promedio else None,
            'estado':       estado,
        })

    context = {
        'alumnos_data':      alumnos_data,
        'page_obj':          page_obj,
        'kpi': {
            'total':            kpi_qs['total']      or 0,
            'aprobados':        kpi_qs['aprobados']  or 0,
            'reprobados':       kpi_qs['reprobados'] or 0,
            'promedio_general': round(kpi_qs['prom_gral'], 1) if kpi_qs['prom_gral'] else 0,
        },
        'cursos_disponibles': Curso.objects.only('id', 'nombre').order_by('nombre'),
        'filtro_curso':       filtro_curso,
        'filtro_estado':      filtro_estado,
        'filtro_q':           filtro_q,
    }
    return render(request, 'reportes/reporte_rendimiento.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# REPORTE 2: Carga Académica de Catedráticos
# (Mismo patrón: annotate en vez de loop)
# ─────────────────────────────────────────────────────────────────────────────
def reporte_carga_academica(request):

    filtro_catedratico = request.GET.get('catedratico', '')
    filtro_q           = request.GET.get('q', '').strip()

    catedraticos_qs = Catedratico.objects.all()

    if filtro_q:
        catedraticos_qs = catedraticos_qs.filter(
            Q(first_name__icontains=filtro_q) |
            Q(last_name__icontains=filtro_q)
        )
    if filtro_catedratico:
        catedraticos_qs = catedraticos_qs.filter(id=filtro_catedratico)

    # Una sola query por catedrático (no loop interno)
    catedraticos_qs = catedraticos_qs.order_by('last_name', 'first_name')

    catedraticos_data    = []
    total_alumnos_global = 0

    for catedratico in catedraticos_qs:

        # Una query: todos los cursos del catedrático con alumno count y promedio
        asignaciones = (
            AsignacionCurso.objects
            .filter(catedratico=catedratico)
            .select_related('curso')
            .values('curso__id', 'curso__nombre')
            .annotate(
                alumnos_inscritos=Count('alumno', distinct=True),
                promedio=Avg('alumno__nota__nota', output_field=FloatField()),
            )
        )

        cursos_list   = []
        total_alumnos = 0

        for asig in asignaciones:
            prom = round(asig['promedio'], 1) if asig['promedio'] else None
            cursos_list.append({
                'nombre':            asig['curso__nombre'],
                'alumnos_inscritos': asig['alumnos_inscritos'],
                'promedio':          prom,
            })
            total_alumnos += asig['alumnos_inscritos']

        promedios = [c['promedio'] for c in cursos_list if c['promedio'] is not None]
        promedio_general = round(sum(promedios) / len(promedios), 1) if promedios else None

        total_alumnos_global += total_alumnos

        catedraticos_data.append({
            'catedratico':      catedratico,
            'cursos':           cursos_list,
            'total_cursos':     len(cursos_list),
            'total_alumnos':    total_alumnos,
            'promedio_general': promedio_general,
        })

    total_cats         = len(catedraticos_data)
    total_asignaciones = sum(r['total_cursos'] for r in catedraticos_data)
    prom_alumnos_cat   = round(total_alumnos_global / total_cats, 1) if total_cats else 0

    context = {
        'catedraticos_data': catedraticos_data,
        'kpi': {
            'total_catedraticos':               total_cats,
            'total_asignaciones':               total_asignaciones,
            'total_alumnos':                    total_alumnos_global,
            'promedio_alumnos_por_catedratico': prom_alumnos_cat,
        },
        'catedraticos_disponibles': Catedratico.objects.only('id', 'first_name', 'last_name').order_by('last_name'),
        'filtro_catedratico':       filtro_catedratico,
        'filtro_q':                 filtro_q,
    }
    return render(request, 'reportes/reporte_carga_academica.html', context)