# Contenido de habitaciones/urls.py
from django.urls import path
from . import views

app_name = 'habitaciones' # Namespace para esta app

urlpatterns = [
    # URL para la lista de todos los tipos de habitación activos
    path('', views.lista_tipos_habitacion_view, name='lista_tipos_habitacion'),

    # URL para el detalle de un tipo de habitación específico, usando su slug
    path('tipo/<slug:slug>/', views.detalle_tipo_habitacion_view, name='detalle_tipo_habitacion'),

    # Podrías añadir más URLs si tienes más vistas, como por ejemplo:
    # path('ofertas/', views.ofertas_habitaciones_view, name='ofertas_habitaciones'),
    # path('buscar/', views.busqueda_avanzada_view, name='busqueda_avanzada_habitaciones'),
]
