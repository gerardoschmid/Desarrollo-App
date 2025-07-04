from django.urls import path
from . import views # Importaremos las vistas más adelante

app_name = 'clientes'

urlpatterns = [
    # CRUD para Clientes (generalmente para el admin o personal del hotel)
    # Estas podrían estar bajo un prefijo como 'gestion/' o ser parte del perfil del cliente.
    path('gestion/', views.ClienteListView.as_view(), name='admin_lista_clientes'),
    path('gestion/nuevo/', views.ClienteCreateView.as_view(), name='admin_crear_cliente'),
    path('gestion/<int:pk>/', views.ClienteDetailView.as_view(), name='admin_detalle_cliente'),
    path('gestion/<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='admin_editar_cliente'),
    path('gestion/<int:pk>/eliminar/', views.ClienteDeleteView.as_view(), name='admin_eliminar_cliente'),

    # URLs para el perfil del cliente (si los clientes pueden registrarse y ver su información)
    # path('perfil/', views.PerfilClienteView.as_view(), name='perfil_cliente'),
    # path('perfil/editar/', views.EditarPerfilClienteView.as_view(), name='editar_perfil_cliente'),
    # path('registro/', views.RegistroClienteView.as_view(), name='registro_cliente'),
]
