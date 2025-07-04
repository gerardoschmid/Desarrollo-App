# Contenido de hotel_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView

# Asegúrate que estas clases existan y sean importables
from core.sitemaps import StaticViewSitemap, HabitacionSitemap, ServicioSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'habitaciones': HabitacionSitemap,
    'servicios': ServicioSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('habitaciones/', include('habitaciones.urls')),
    path('reservas/', include('reservas.urls')),
    path('servicios/', include('servicios.urls')),
    path('clientes/', include('clientes.urls')), # Aunque no tenga vistas frontend, puede tener admin

    # URLs para sitemap y robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # Servir robots.txt usando TemplateView para poder usar variables de contexto si es necesario
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # Para login/logout si usas django.contrib.auth.views
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    # Servir archivos de media en desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Servir archivos estáticos (aunque Django lo hace automáticamente si APP_DIRS=True y no hay STATIC_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])


    # Si usas debug_toolbar:
    # try:
    #     import debug_toolbar
    #     urlpatterns = [
    #         path('__debug__/', include(debug_toolbar.urls)),
    #     ] + urlpatterns
    # except ImportError:
    #     pass
