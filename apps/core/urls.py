from django.urls import path
from . import views # Importaremos las vistas más adelante

app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='inicio'), # Página de inicio
    path('sobre-nosotros/', views.SobreNosotrosPageView.as_view(), name='sobre_nosotros'),
    path('contacto/', views.ContactoPageView.as_view(), name='contacto'),
    path('galeria/', views.GaleriaPageView.as_view(), name='galeria'),
    # path('enviar-contacto/', views.enviar_mensaje_contacto, name='enviar_contacto'), # Para el form de contacto
]
