from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario extendido con roles.
    Roles disponibles: admin, operador
    """

    ROL_ADMIN = 'admin'
    ROL_OPERADOR = 'operador'

    ROLES = [
        (ROL_ADMIN, 'Administrador'),
        (ROL_OPERADOR, 'Operador'),
    ]

    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default=ROL_OPERADOR,
        verbose_name='Rol',
    )

    def es_admin(self):
        return self.rol == self.ROL_ADMIN

    def es_operador(self):
        return self.rol == self.ROL_OPERADOR

    def __str__(self):
        return f'{self.username} ({self.get_rol_display()})'

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
