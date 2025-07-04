from django.urls import path
from . import views # Importaremos las vistas más adelante

app_name = 'servicios'

urlpatterns = [
    # Listado público de servicios
    path('', views.ListaServiciosView.as_view(), name='lista_servicios'),
    path('<int:pk>/', views.DetalleServicioView.as_view(), name='detalle_servicio'), # Detalle público de un servicio

    # CRUD para Servicios (generalmente para el admin o personal del hotel)
    # Estas podrían estar bajo un prefijo como 'gestion/'
    path('gestion/', views.ServicioListView.as_view(), name='admin_lista_servicios'),
    path('gestion/nuevo/', views.ServicioCreateView.as_view(), name='admin_crear_servicio'),
    path('gestion/<int:pk>/detalle/', views.ServicioDetailView.as_view(), name='admin_detalle_servicio'), # Vista de detalle para admin
    path('gestion/<int:pk>/editar/', views.ServicioUpdateView.as_view(), name='admin_editar_servicio'),
    path('gestion/<int:pk>/eliminar/', views.ServicioDeleteView.as_view(), name='admin_eliminar_servicio'),
]
