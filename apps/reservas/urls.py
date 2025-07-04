from django.urls import path
from . import views # Importaremos las vistas más adelante

app_name = 'reservas'

urlpatterns = [
    # Formulario de búsqueda de disponibilidad y creación de reserva (frontend para clientes)
    path('crear/', views.CrearReservaView.as_view(), name='crear_reserva'),
    path('confirmacion/<int:pk>/', views.ConfirmacionReservaView.as_view(), name='confirmacion_reserva'),

    # Listado de reservas del cliente (requiere autenticación)
    # path('mis-reservas/', views.MisReservasListView.as_view(), name='mis_reservas'),

    # CRUD para Reservas (generalmente para el admin o personal del hotel)
    # Estas podrían estar bajo un prefijo como 'gestion/'
    path('gestion/', views.ReservaListView.as_view(), name='admin_lista_reservas'),
    path('gestion/nueva/', views.ReservaCreateView.as_view(), name='admin_crear_reserva'), # Para personal
    path('gestion/<int:pk>/', views.ReservaDetailView.as_view(), name='admin_detalle_reserva'),
    path('gestion/<int:pk>/editar/', views.ReservaUpdateView.as_view(), name='admin_editar_reserva'),
    path('gestion/<int:pk>/cancelar/', views.CancelarReservaView.as_view(), name='admin_cancelar_reserva'), # Podría ser una vista específica
    path('gestion/<int:pk>/eliminar/', views.ReservaDeleteView.as_view(), name='admin_eliminar_reserva'),

    # API o endpoint para verificar disponibilidad (podría ser útil para JavaScript en el frontend)
    path('api/verificar-disponibilidad/', views.verificar_disponibilidad_api, name='api_verificar_disponibilidad'),
]
