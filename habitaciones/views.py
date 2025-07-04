# Contenido de habitaciones/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import TipoHabitacion # Ya no se necesita Habitacion aquí directamente para estas vistas
# from core.views import get_site_config # Ya no es necesario, config viene del context processor

# Vista basada en función para la lista de tipos de habitación
def lista_tipos_habitacion_view(request):
    # config = get_site_config() # Config se inyecta globalmente
    tipos_habitacion = TipoHabitacion.objects.filter(activo=True).prefetch_related('imagenes_adicionales', 'amenidades')

    context = {
        # 'config': config,
        'tipos_habitacion': tipos_habitacion,
        # 'page_title': f"Nuestros Tipos de Habitación - {config.nombre_hotel if config else 'Hotel Premium MVP'}",
    }
    return render(request, 'habitaciones/habitacion_list.html', context)

# Vista basada en función para el detalle de un tipo de habitación
def detalle_tipo_habitacion_view(request, slug):
    # config = get_site_config() # Config se inyecta globalmente
    # Usar prefetch_related para optimizar la carga de imágenes y amenidades
    tipo_habitacion = get_object_or_404(
        TipoHabitacion.objects.prefetch_related('imagenes_adicionales', 'amenidades'),
        slug=slug,
        activo=True
    )

    # Podrías querer mostrar habitaciones físicas disponibles de este tipo,
    # pero eso se manejaría mejor en el flujo de reserva o con una consulta AJAX más específica.
    # Para esta vista de detalle, nos centramos en el TIPO de habitación.

    context = {
        # 'config': config,
        'tipo_habitacion': tipo_habitacion,
        # 'page_title': f"{tipo_habitacion.nombre} - {config.nombre_hotel if config else 'Hotel Premium MVP'}",
    }
    return render(request, 'habitaciones/habitacion_detail.html', context)


# Alternativa usando Class-Based Views (ListView y DetailView)
# Descomenta y usa estas si prefieres este enfoque. Asegúrate de actualizar urls.py también.

# class TipoHabitacionListView(ListView):
#     model = TipoHabitacion
#     template_name = 'habitaciones/habitacion_list.html'
#     context_object_name = 'tipos_habitacion'
#     # Filtrar solo los activos y optimizar consultas
#     queryset = TipoHabitacion.objects.filter(activo=True).prefetch_related('imagenes_adicionales', 'amenidades')
#     paginate_by = 6 # Ejemplo de paginación

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # config = get_site_config() # Config se inyecta globalmente
    #     # context['config'] = config # Ya no es necesario
    #     # context['page_title'] = f"Nuestros Tipos de Habitación - {context['config'].nombre_hotel if context.get('config') else 'Hotel Premium MVP'}"
    #     return context

# class TipoHabitacionDetailView(DetailView):
#     model = TipoHabitacion
#     template_name = 'habitaciones/habitacion_detail.html'
#     context_object_name = 'tipo_habitacion'
#     slug_field = 'slug' # Campo en el modelo a usar para la búsqueda
#     slug_url_kwarg = 'slug' # Nombre del parámetro en la URL que contiene el slug

#     # Filtrar solo los activos y optimizar consultas
#     queryset = TipoHabitacion.objects.filter(activo=True).prefetch_related('imagenes_adicionales', 'amenidades')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # config = get_site_config() # Config se inyecta globalmente
    #     # context['config'] = config # Ya no es necesario
    #     # context['page_title'] = f"{self.object.nombre} - {context['config'].nombre_hotel if context.get('config') else 'Hotel Premium MVP'}"
    #     return context

# Si decides usar las Class-Based Views, actualiza tus urls.py para llamarlas:
# path('', views.TipoHabitacionListView.as_view(), name='lista_tipos_habitacion'),
# path('tipo/<slug:slug>/', views.TipoHabitacionDetailView.as_view(), name='detalle_tipo_habitacion'),
```
