# Contenido de habitaciones/apps.py
from django.apps import AppConfig


class HabitacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'habitaciones'
    verbose_name = '2. Gestión de Habitaciones' # El número ayuda a ordenar en el admin (si es un criterio)
