# Contenido de core/views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView # DetailView no se usa directamente aquí para core
from django.contrib import messages
from django.urls import reverse_lazy

from .models import ConfiguracionSitio, ImagenGaleria # MensajeContacto se maneja en el form
from .forms import ContactoForm

# Importar modelos de otras apps para la página de inicio
from habitaciones.models import TipoHabitacion
from servicios.models import Servicio

# Esta función se usaba para obtener la configuración, ahora usamos un context processor
# def get_site_config():
#     """ Obtiene la primera (y única) instancia de ConfiguracionSitio. """
#     return ConfiguracionSitio.objects.first()

def index_view(request):
    # config = get_site_config() # Ya no es necesario aquí, viene del context processor

    # Obtener tipos de habitación destacados (ej. los 3 más recientes o marcados como destacados)
    # Asume que el modelo TipoHabitacion tiene un campo booleano 'destacado' y 'activo'
    tipos_habitacion_destacados = TipoHabitacion.objects.filter(activo=True, destacado=True).order_by('-fecha_actualizacion')[:3]

    # Obtener servicios destacados (ej. los 4 más relevantes o marcados)
    # Asume que el modelo Servicio tiene un campo booleano 'destacado' y 'disponible'
    servicios_destacados = Servicio.objects.filter(disponible=True, destacado=True).order_by('?')[:4] # '?' para aleatorio, o por orden/fecha

    # Últimas imágenes de la galería para un pequeño preview (opcional)
    ultimas_imagenes_galeria = ImagenGaleria.objects.order_by('-orden', '-id')[:4] # Ordenadas por 'orden' y luego por ID descendente

    context = {
        # 'config': config, # Se inyecta globalmente
        'tipos_habitacion_destacados': tipos_habitacion_destacados,
        'servicios_destacados': servicios_destacados,
        'ultimas_imagenes_galeria': ultimas_imagenes_galeria,
        # 'page_title': f"Bienvenido a {config.nombre_hotel if config else 'Hotel Premium MVP'}", # El título se puede manejar en la plantilla base
    }
    return render(request, 'core/index.html', context)

def about_view(request):
    # config = get_site_config()
    context = {
        # 'config': config,
        # 'page_title': f"Sobre Nosotros - {config.nombre_hotel if config else 'Hotel Premium MVP'}",
    }
    return render(request, 'core/about.html', context)

def contact_view(request):
    # config = get_site_config()
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.')
            return redirect('core:contact') # Redirige a la misma página para limpiar el formulario
        else:
            # Si el formulario no es válido, se mostrarán los errores en la plantilla.
            messages.error(request, 'Hubo un error en el formulario. Por favor, revisa los campos marcados.')
    else:
        form = ContactoForm()

    context = {
        # 'config': config,
        'form': form,
        # 'page_title': f"Contacto - {config.nombre_hotel if config else 'Hotel Premium MVP'}",
    }
    return render(request, 'core/contacto.html', context)

class GalleryListView(ListView):
    model = ImagenGaleria
    template_name = 'core/gallery.html'
    context_object_name = 'imagenes'
    paginate_by = 12 # Mostrar 12 imágenes por página, por ejemplo
    queryset = ImagenGaleria.objects.order_by('orden', '-id') # Ordenar por el campo 'orden' y luego por ID

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     config = get_site_config()
    #     context['config'] = config
    #     context['page_title'] = f"Galería - {config.nombre_hotel if config else 'Hotel Premium MVP'}"
    #     return context

gallery_view = GalleryListView.as_view()


# Ejemplo de una vista que requiere que exista la configuración del sitio
# def una_vista_que_necesita_config(request):
#     config = ConfiguracionSitio.objects.first()
#     if not config:
#         # Opción 1: Redirigir a una página de setup o mostrar un mensaje
#         messages.warning(request, "La configuración del sitio aún no ha sido establecida. Por favor, configurela en el panel de administración.")
#         # return redirect('alguna_pagina_de_error_o_setup')
#         # Opción 2: Usar valores por defecto o levantar un error si es crítico
#         # Para este MVP, las plantillas usan el filtro `default` si config es None.
#         pass
#     # ... resto de la lógica de la vista
#     return render(request, 'alguna_plantilla.html', {'config': config})
