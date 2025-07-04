from django.urls import path
from . import views # Importaremos las vistas más adelante

app_name = 'habitaciones'

urlpatterns = [
    # Listado público de tipos de habitación o galería principal de habitaciones
    path('', views.ListaTiposHabitacionView.as_view(), name='lista_tipos_habitacion'),
    path('tipo/<int:pk>/', views.DetalleTipoHabitacionView.as_view(), name='detalle_tipo_habitacion'), # Detalle de un tipo de habitación

    # CRUD para Habitaciones (generalmente para el admin o personal del hotel)
    # Estas podrían estar bajo un prefijo como 'gestion/' si son solo para backend.
    # Por ahora, las dejaré así para simplificar.
    path('gestion/', views.HabitacionListView.as_view(), name='admin_lista_habitaciones'),
    path('gestion/nueva/', views.HabitacionCreateView.as_view(), name='admin_crear_habitacion'),
    path('gestion/<str:numero_habitacion>/', views.HabitacionDetailView.as_view(), name='admin_detalle_habitacion'),
    path('gestion/<str:numero_habitacion>/editar/', views.HabitacionUpdateView.as_view(), name='admin_editar_habitacion'),
    path('gestion/<str:numero_habitacion>/eliminar/', views.HabitacionDeleteView.as_view(), name='admin_eliminar_habitacion'),

    # URLs para imágenes de habitación (si se necesita un CRUD específico para ellas)
    # path('gestion/<str:numero_habitacion>/imagenes/', views.ImagenHabitacionListView.as_view(), name='admin_lista_imagenes_habitacion'),
    # path('gestion/<str:numero_habitacion>/imagenes/nueva/', views.ImagenHabitacionCreateView.as_view(), name='admin_crear_imagen_habitacion'),
    # path('gestion/imagenes/<int:pk>/editar/', views.ImagenHabitacionUpdateView.as_view(), name='admin_editar_imagen_habitacion'),
    # path('gestion/imagenes/<int:pk>/eliminar/', views.ImagenHabitacionDeleteView.as_view(), name='admin_eliminar_imagen_habitacion'),

    # CRUD para Tipos de Habitación (si se gestionan desde el frontend y no solo el admin)
    # path('gestion/tipos/', views.TipoHabitacionListView.as_view(), name='admin_lista_tipos'),
    # path('gestion/tipos/nuevo/', views.TipoHabitacionCreateView.as_view(), name='admin_crear_tipo'),
    # path('gestion/tipos/<int:pk>/editar/', views.TipoHabitacionUpdateView.as_view(), name='admin_editar_tipo'),
    # path('gestion/tipos/<int:pk>/eliminar/', views.TipoHabitacionDeleteView.as_view(), name='admin_eliminar_tipo'),
]
