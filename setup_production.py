#!/usr/bin/env python
"""
Script que se ejecuta al inicio del servidor para configurar datos iniciales
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
django.setup()

from core.models import Usuario
from gestion_inventario.models import Categoria, Proveedor, Producto

def setup_production():
    """Configurar datos iniciales en producción"""
    print("🚀 Configurando producción...")
    
    try:
        # Crear superusuario si no existe
        if not Usuario.objects.filter(is_superuser=True).exists():
            admin_user = Usuario.objects.create_superuser(
                username='admin',
                email='admin@inventario.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                rol='admin'
            )
            print(f"✅ Superusuario creado: {admin_user.username}")
        else:
            print("✅ Superusuario ya existe")
        
        # Crear datos iniciales si no existen
        if not Categoria.objects.exists():
            # Crear categorías
            cat1 = Categoria.objects.create(
                nombre='Electrónicos',
                descripcion='Productos electrónicos y tecnológicos'
            )
            cat2 = Categoria.objects.create(
                nombre='Hogar',
                descripcion='Productos para el hogar'
            )
            
            # Crear proveedores
            prov1 = Proveedor.objects.create(
                nombre='TechSupply',
                telefono='555-0001',
                email='ventas@techsupply.com',
                direccion='Av. Tecnología 123'
            )
            
            # Crear productos
            Producto.objects.create(
                nombre='Laptop Dell',
                descripcion='Laptop Dell Inspiron 15',
                precio=15000.00,
                stock=10,
                stock_minimo=2,
                categoria=cat1,
                proveedor=prov1
            )
            
            # Crear usuario operador
            if not Usuario.objects.filter(username='operador').exists():
                operador = Usuario.objects.create_user(
                    username='operador',
                    email='operador@inventario.com',
                    password='operador123',
                    first_name='Juan',
                    last_name='Pérez',
                    rol='operador'
                )
                print(f"✅ Usuario operador creado: {operador.username}")
            
            print("✅ Datos iniciales cargados")
            print(f"   - Categorías: {Categoria.objects.count()}")
            print(f"   - Proveedores: {Proveedor.objects.count()}")
            print(f"   - Productos: {Producto.objects.count()}")
        else:
            print("✅ Datos iniciales ya existen")
        
        print("🎉 Configuración de producción completada")
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        # No fallar el inicio del servidor por esto
        pass

if __name__ == '__main__':
    setup_production()