from django.db import models
from django.contrib.auth.models import User # O un modelo de usuario personalizado si es necesario
from django.utils.translation import gettext_lazy as _

# Podríamos extender el User model de Django o tener un perfil separado.
# Por simplicidad, crearemos un modelo Cliente que puede o no estar ligado a un User.
# Si se requiere que los clientes se registren, una relación OneToOneField con User es recomendada.

class Cliente(models.Model):
    # Si se integra con django.contrib.auth.models.User:
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Usuario"))

    nombre = models.CharField(_("Nombre"), max_length=100)
    apellidos = models.CharField(_("Apellidos"), max_length=100)
    email = models.EmailField(_("Email"), unique=True) # Considerar si debe ser único o no, dependiendo de si un email puede tener múltiples perfiles de cliente (poco común)
    telefono = models.CharField(_("Teléfono"), max_length=20, blank=True, null=True)
    # direccion = models.TextField(_("Dirección"), blank=True, null=True) # Opcional

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("Clientes")
        ordering = ['apellidos', 'nombre']

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellidos}"
