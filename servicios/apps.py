# Contenido de servicios/apps.py
from django.apps import AppConfig


class ServiciosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicios'
    verbose_name = '5. Servicios del Hotel' # El número ayuda a ordenar en el admin si se desea
```
