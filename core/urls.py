# Contenido de core/urls.py
from django.urls import path
from . import views

app_name = 'core' # Define el namespace para esta app

urlpatterns = [
    path('', views.index_view, name='index'),
    path('sobre-nosotros/', views.about_view, name='about'),
    path('contacto/', views.contact_view, name='contact'),
    path('galeria/', views.gallery_view, name='gallery'),

    # Ejemplo de URL para un posible panel de admin personalizado si no usas el de Django
    # path('dashboard/', views.dashboard_view, name='dashboard'),
]
