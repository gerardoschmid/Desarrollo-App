"""
URL configuration for hotel_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/X.Y/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _

# Personalizar títulos del Admin
admin.site.site_header = _("Administración Hotel Premium")
admin.site.site_title = _("Portal de Administración del Hotel")
admin.site.index_title = _("Bienvenido al Portal de Administración")

urlpatterns = [
    path('admin/', admin.site.urls),
    # URLs de la app core (página de inicio, sobre nosotros, contacto, etc.)
    path('', include('core.urls', namespace='core')),
    # URLs de las otras apps
    path('habitaciones/', include('habitaciones.urls', namespace='habitaciones')),
    path('reservas/', include('reservas.urls', namespace='reservas')),
    path('clientes/', include('clientes.urls', namespace='clientes')),
    path('servicios/', include('servicios.urls', namespace='servicios')),
    # Aquí podrías añadir URLs para autenticación si es necesario
    # path('cuentas/', include('django.contrib.auth.urls')), # URLs de autenticación de Django
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else settings.STATICFILES_DIRS[0])

# Nota sobre los namespaces:
# Usar namespaces (ej. namespace='core') es una buena práctica para evitar colisiones de nombres de URL
# entre diferentes aplicaciones. Luego puedes referenciar URLs en templates como {% url 'core:nombre_url' %}.
# Para que esto funcione, en cada archivo urls.py de las apps, necesitas definir un app_name.
# Ejemplo en apps/core/urls.py:
# app_name = 'core'
# urlpatterns = [ ... ]
