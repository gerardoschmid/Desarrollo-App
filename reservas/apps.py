# Contenido de reservas/apps.py
from django.apps import AppConfig


class ReservasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservas'
    verbose_name = '3. Gestión de Reservas' # El número ayuda a ordenar en el admin

    def ready(self):
        try:
            import reservas.signals # Importar señales si las tienes
        except ImportError:
            pass # No hacer nada si el archivo de señales no existe aún
```
