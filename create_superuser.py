#!/usr/bin/env python
"""
Script para crear superusuario automáticamente en producción
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
django.setup()

from core.models import Usuario

def create_superuser():
    """Crear superusuario si no existe"""
    try:
        # Verificar si ya existe un superusuario
        if Usuario.objects.filter(is_superuser=True).exists():
            print("✅ Superusuario ya existe")
            return
        
        # Crear superusuario
        admin_user = Usuario.objects.create_superuser(
            username='admin',
            email='admin@inventario.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            rol='admin'
        )
        
        print("✅ Superusuario creado exitosamente:")
        print(f"   Usuario: {admin_user.username}")
        print(f"   Email: {admin_user.email}")
        print(f"   Rol: {admin_user.rol}")
        
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")

if __name__ == '__main__':
    create_superuser()