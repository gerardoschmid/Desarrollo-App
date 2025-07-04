# Contenido de clientes/urls.py
from django.urls import path
# from . import views # Descomentar si añades vistas para clientes en el frontend

app_name = 'clientes' # Namespace para esta app

urlpatterns = [
    # Por ahora, esta app no tiene vistas públicas (frontend) definidas.
    # Si se implementara un área de clientes, aquí irían sus URLs.
    # Ejemplo:
    # path('mi-cuenta/', views.vista_cuenta_cliente, name='mi_cuenta'),
    # path('mis-reservas/', views.lista_reservas_cliente, name='mis_reservas_cliente'),
]
