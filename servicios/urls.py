# Contenido de servicios/urls.py
from django.urls import path
from . import views

app_name = 'servicios' # Namespace para esta app

urlpatterns = [
    # URL para la lista de todos los servicios disponibles, agrupados por categoría
    path('', views.lista_servicios_view, name='lista_servicios'),

    # URL para el detalle de un servicio específico, usando su slug
    path('<slug:slug>/', views.detalle_servicio_view, name='detalle_servicio'),

    # Podrías añadir una URL para ver servicios por categoría si lo deseas:
    # path('categoria/<slug:categoria_slug>/', views.lista_servicios_por_categoria_view, name='servicios_por_categoria'),
]
