# reportes/views.py
from django.shortcuts import render
from django.db.models import Avg, Q

# ── Imports con el prefijo completo igual que el resto del proyecto ───────────
from universidad.Models.Alumno.models import Alumno
from universidad.Models.Curso.models import Curso
from universidad.Models.catedratico.models import Catedratico
from universidad.Models.Notas.models import Nota
from universidad.Models.Inscripcion_alumno.models import InscripcionAlumno
from universidad.Models.asignacion_curso.models import AsignacionCurso


# ─────────────────────────────────────────────────────────────────────────────
# REPORTE 1: Rendimiento Académico por Alumno
# Consulta combinada: Alumno → InscripcionAlumno → AsignacionCurso → Nota
# ─────────────────────────────────────────────────────────────────────────────
def reporte_rendimiento(request):

    # ── Filtros desde GET ─────────────────────────────────────────────────────
    filtro_ciclo  = request.GET.get('ciclo', '')
    filtro_curso  = request.GET.get('curso', '')
    filtro_estado = request.GET.get('estado', '')
    filtro_q      = request.GET.get('q', '').strip()

    # ── QuerySet base de alumnos ──────────────────────────────────────────────
    alumnos_qs = Alumno.objects.all()

    if filtro_q:
        alumnos_qs = alumnos_qs.filter(
            Q(nombre__icontains=filtro_q) |
            Q(apellido__icontains=filtro_q) |
            Q(carne__icontains=filtro_q)
        )

    # ── Construir datos enriquecidos por alumno ───────────────────────────────
    alumnos_data = []

    for alumno in alumnos_qs.order_by('apellido', 'nombre'):

        # JOIN: InscripcionAlumno → AsignacionCurso → Curso
        inscripciones_qs = InscripcionAlumno.objects.filter(
            alumno=alumno
        ).select_related('asignacion_curso', 'asignacion_curso__curso')

        if filtro_ciclo:
            inscripciones_qs = inscripciones_qs.filter(
                asignacion_curso__ciclo=filtro_ciclo
            )
        if filtro_curso:
            inscripciones_qs = inscripciones_qs.filter(
                asignacion_curso__curso_id=filtro_curso
            )

        total_cursos = inscripciones_qs.count()

        # JOIN: Nota → InscripcionAlumno → AsignacionCurso
        notas_qs = Nota.objects.filter(
            inscripcion_alumno__alumno=alumno
        )
        if filtro_ciclo:
            notas_qs = notas_qs.filter(
                inscripcion_alumno__asignacion_curso__ciclo=filtro_ciclo
            )
        if filtro_curso:
            notas_qs = notas_qs.filter(
                inscripcion_alumno__asignacion_curso__curso_id=filtro_curso
            )

        total_notas = notas_qs.count()
        promedio    = notas_qs.aggregate(promedio=Avg('nota'))['promedio']

        # Determinar estado
        if promedio is None:
            estado = 'sin_notas'
        elif promedio >= 61:
            estado = 'aprobado'
        else:
            estado = 'reprobado'

        # Aplicar filtro de estado
        if filtro_estado and filtro_estado != estado:
            continue

        alumnos_data.append({
            'alumno':       alumno,
            'total_cursos': total_cursos,
            'total_notas':  total_notas,
            'promedio':     promedio,
            'estado':       estado,
        })

    # ── KPIs globales ─────────────────────────────────────────────────────────
    total      = len(alumnos_data)
    aprobados  = sum(1 for r in alumnos_data if r['estado'] == 'aprobado')
    reprobados = sum(1 for r in alumnos_data if r['estado'] == 'reprobado')

    promedios_validos = [r['promedio'] for r in alumnos_data if r['promedio'] is not None]
    promedio_general  = (sum(promedios_validos) / len(promedios_validos)) if promedios_validos else 0

    # ── Datos para los selectores de filtro ───────────────────────────────────
    ciclos_disponibles = (
        AsignacionCurso.objects
        .values_list('ciclo', flat=True)
        .distinct()
        .order_by('-ciclo')
    )
    cursos_disponibles = Curso.objects.all().order_by('nombre')

    context = {
        'alumnos_data': alumnos_data,
        'kpi': {
            'total':            total,
            'aprobados':        aprobados,
            'reprobados':       reprobados,
            'promedio_general': promedio_general,
        },
        'ciclos_disponibles':  ciclos_disponibles,
        'cursos_disponibles':  cursos_disponibles,
        'filtro_ciclo':        filtro_ciclo,
        'filtro_curso':        filtro_curso,
        'filtro_estado':       filtro_estado,
        'filtro_q':            filtro_q,
    }
    return render(request, 'reportes/reporte_rendimiento.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# REPORTE 2: Carga Académica de Catedráticos
# Consulta combinada: Catedratico → AsignacionCurso → Curso
#                                 → InscripcionAlumno → Nota
# ─────────────────────────────────────────────────────────────────────────────
def reporte_carga_academica(request):

    # ── Filtros desde GET ─────────────────────────────────────────────────────
    filtro_ciclo       = request.GET.get('ciclo', '')
    filtro_catedratico = request.GET.get('catedratico', '')
    filtro_q           = request.GET.get('q', '').strip()

    # ── QuerySet base de catedráticos ────────────────────────────────────────
    catedraticos_qs = Catedratico.objects.all()

    if filtro_q:
        catedraticos_qs = catedraticos_qs.filter(
            Q(nombre__icontains=filtro_q) |
            Q(apellido__icontains=filtro_q)
        )
    if filtro_catedratico:
        catedraticos_qs = catedraticos_qs.filter(id=filtro_catedratico)

    # ── Construir datos enriquecidos por catedrático ──────────────────────────
    catedraticos_data    = []
    total_alumnos_global = 0

    for catedratico in catedraticos_qs.order_by('apellido', 'nombre'):

        # JOIN: AsignacionCurso → Curso
        asignaciones_qs = AsignacionCurso.objects.filter(
            catedratico=catedratico
        ).select_related('curso')

        if filtro_ciclo:
            asignaciones_qs = asignaciones_qs.filter(ciclo=filtro_ciclo)

        cursos_list   = []
        total_alumnos = 0

        for asig in asignaciones_qs:

            # COUNT: alumnos inscritos en esta asignación
            alumnos_inscritos = InscripcionAlumno.objects.filter(
                asignacion_curso=asig
            ).count()

            # AVG: promedio de notas del curso
            promedio_curso = Nota.objects.filter(
                inscripcion_alumno__asignacion_curso=asig
            ).aggregate(promedio=Avg('nota'))['promedio']

            cursos_list.append({
                'nombre':            asig.curso.nombre,
                'ciclo':             asig.ciclo,
                'alumnos_inscritos': alumnos_inscritos,
                'promedio':          promedio_curso,
            })

            total_alumnos += alumnos_inscritos

        # Promedio general del catedrático sobre todos sus cursos
        promedios = [c['promedio'] for c in cursos_list if c['promedio'] is not None]
        promedio_general = (sum(promedios) / len(promedios)) if promedios else None

        total_alumnos_global += total_alumnos

        catedraticos_data.append({
            'catedratico':      catedratico,
            'cursos':           cursos_list,
            'total_cursos':     len(cursos_list),
            'total_alumnos':    total_alumnos,
            'promedio_general': promedio_general,
        })

    # ── KPIs globales ─────────────────────────────────────────────────────────
    total_cats         = len(catedraticos_data)
    total_asignaciones = sum(r['total_cursos'] for r in catedraticos_data)
    prom_alumnos_cat   = (total_alumnos_global / total_cats) if total_cats else 0

    # ── Datos para los selectores de filtro ───────────────────────────────────
    ciclos_disponibles = (
        AsignacionCurso.objects
        .values_list('ciclo', flat=True)
        .distinct()
        .order_by('-ciclo')
    )
    catedraticos_disponibles = Catedratico.objects.all().order_by('apellido', 'nombre')

    context = {
        'catedraticos_data': catedraticos_data,
        'kpi': {
            'total_catedraticos':               total_cats,
            'total_asignaciones':               total_asignaciones,
            'total_alumnos':                    total_alumnos_global,
            'promedio_alumnos_por_catedratico': prom_alumnos_cat,
        },
        'ciclos_disponibles':       ciclos_disponibles,
        'catedraticos_disponibles': catedraticos_disponibles,
        'filtro_ciclo':             filtro_ciclo,
        'filtro_catedratico':       filtro_catedratico,
        'filtro_q':                 filtro_q,
    }
    return render(request, 'reportes/reporte_carga_academica.html', context)