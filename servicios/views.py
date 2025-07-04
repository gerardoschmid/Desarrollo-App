# Contenido de servicios/views.py
from django.shortcuts import render, get_object_or_404
from .models import Servicio, CategoriaServicio
# from core.views import get_site_config # Ya no es necesario, config viene del context processor

# Vista basada en función para la lista de servicios, agrupados por categoría
def lista_servicios_view(request):
    # config = get_site_config() # Config se inyecta globalmente

    # Obtener todas las categorías que tienen al menos un servicio disponible, ordenadas
    categorias_con_servicios = CategoriaServicio.objects.filter(
        servicios__disponible=True # Filtra categorías que tienen servicios disponibles
    ).distinct().order_by('orden', 'nombre').prefetch_related(
        models.Prefetch(
            'servicios',
            queryset=Servicio.objects.filter(disponible=True).order_by('nombre'), # Solo servicios disponibles dentro de cada categoría
            to_attr='servicios_disponibles_list' # Nombre del atributo para acceder a esta lista pre-cargada
        )
    )

    # Si no quieres agrupar por categoría y solo quieres una lista plana de servicios:
    # servicios_todos = Servicio.objects.filter(disponible=True).order_by('categoria__orden', 'nombre').select_related('categoria')

    servicios_por_categoria = []
    for cat in categorias_con_servicios:
        # Usar la lista pre-cargada 'servicios_disponibles_list'
        if hasattr(cat, 'servicios_disponibles_list') and cat.servicios_disponibles_list:
            servicios_por_categoria.append((cat, cat.servicios_disponibles_list))

    context = {
        # 'config': config,
        'servicios_por_categoria': servicios_por_categoria, # Lista de tuplas (categoria, [servicios_de_esa_categoria])
        # 'servicios_todos': servicios_todos, # Descomentar y usar si prefieres lista plana
        # 'page_title': f"Nuestros Servicios - {config.nombre_hotel if config else 'Hotel Premium MVP'}",
    }
    return render(request, 'servicios/servicio_list.html', context)

# Vista basada en función para el detalle de un servicio
def detalle_servicio_view(request, slug):
    # config = get_site_config() # Config se inyecta globalmente
    servicio = get_object_or_404(Servicio.objects.select_related('categoria'), slug=slug, disponible=True)

    # Podrías obtener otros servicios de la misma categoría para mostrar como sugerencias
    servicios_relacionados = []
    if servicio.categoria:
        servicios_relacionados = Servicio.objects.filter(
            categoria=servicio.categoria,
            disponible=True
        ).exclude(pk=servicio.pk).order_by('?')[:3] # 3 aleatorios, o por nombre/orden

    context = {
        # 'config': config,
        'servicio': servicio,
        'servicios_relacionados': servicios_relacionados,
        # 'page_title': f"{servicio.nombre} - {config.nombre_hotel if config else 'Hotel Premium MVP'}",
    }
    return render(request, 'servicios/servicio_detail.html', context)

# Si prefieres Class-Based Views (requiere ajustar la lógica de agrupación para la lista):

# from django.views.generic import ListView, DetailView
# from django.db import models

# class ServicioListView(ListView):
#     # Este ListView simple no agrupará por categoría directamente.
#     # Para agrupar, necesitarías sobrescribir get_context_data o get_queryset
#     # de forma más compleja, o pasar a una TemplateView y construir el contexto manualmente.
#     model = Servicio
#     template_name = 'servicios/servicio_list.html'
#     context_object_name = 'servicios_todos' # Si usas una lista plana
#     queryset = Servicio.objects.filter(disponible=True).select_related('categoria').order_by('categoria__orden', 'nombre')
#     paginate_by = 9

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Para agrupar por categoría aquí:
    #     categorias = CategoriaServicio.objects.filter(
    #         servicios__disponible=True
    #     ).distinct().order_by('orden', 'nombre').prefetch_related(
    #         models.Prefetch('servicios', queryset=Servicio.objects.filter(disponible=True), to_attr='servicios_list')
    #     )
    #     servicios_agrupados = []
    #     for cat in categorias:
    #         if cat.servicios_list: # Solo añadir si la categoría tiene servicios después del prefetch
    #             servicios_agrupados.append((cat, cat.servicios_list))

    #     context['servicios_por_categoria'] = servicios_agrupados
    #     # context['page_title'] = "Nuestros Servicios"
    #     return context

# class ServicioDetailView(DetailView):
#     model = Servicio
#     template_name = 'servicios/servicio_detail.html'
#     context_object_name = 'servicio'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     queryset = Servicio.objects.filter(disponible=True).select_related('categoria')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     servicio = self.object
    #     if servicio.categoria:
    #         context['servicios_relacionados'] = Servicio.objects.filter(
    #             categoria=servicio.categoria, disponible=True
    #         ).exclude(pk=servicio.pk).order_by('?')[:3]
    #     # context['page_title'] = servicio.nombre
    #     return context

# Si usas CBV, actualiza urls.py:
# path('', views.ServicioListView.as_view(), name='lista_servicios'),
# path('<slug:slug>/', views.ServicioDetailView.as_view(), name='detalle_servicio'),
```
