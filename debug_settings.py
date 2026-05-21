#!/usr/bin/env python
"""
Script de debug para verificar configuración en producción
"""
import os
import sys

def check_environment():
    """Verificar variables de entorno"""
    print("=== VERIFICACIÓN DE ENTORNO ===")
    
    # Variables críticas
    critical_vars = [
        'SECRET_KEY',
        'DEBUG', 
        'DATABASE_URL',
        'RENDER_EXTERNAL_HOSTNAME'
    ]
    
    for var in critical_vars:
        value = os.environ.get(var, 'NO DEFINIDA')
        if var == 'SECRET_KEY' and value != 'NO DEFINIDA':
            print(f"{var}: {'*' * 20} (oculta)")
        else:
            print(f"{var}: {value}")
    
    print("\n=== VERIFICACIÓN DE DJANGO ===")
    try:
        import django
        print(f"Django version: {django.get_version()}")
        
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
        django.setup()
        
        from django.conf import settings
        print(f"DEBUG: {settings.DEBUG}")
        print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
        
        # Test database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Conexión a base de datos: OK")
            
    except Exception as e:
        print(f"❌ Error en Django: {e}")
        return False
    
    print("\n=== VERIFICACIÓN DE MODELOS ===")
    try:
        from core.models import Usuario
        from gestion_inventario.models import Categoria, Proveedor, Producto
        
        print(f"Usuarios: {Usuario.objects.count()}")
        print(f"Categorías: {Categoria.objects.count()}")
        print(f"Proveedores: {Proveedor.objects.count()}")
        print(f"Productos: {Producto.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        return False
    
    print("\n✅ Todas las verificaciones completadas")
    return True

if __name__ == '__main__':
    success = check_environment()
    sys.exit(0 if success else 1)