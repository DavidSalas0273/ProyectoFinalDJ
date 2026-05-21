#!/usr/bin/env python
"""
Script para cargar datos iniciales en producción
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
django.setup()

from gestion_inventario.models import Categoria, Proveedor, Producto
from core.models import Usuario

def load_initial_data():
    """Cargar datos iniciales si no existen"""
    try:
        # Solo cargar si no hay datos
        if Categoria.objects.exists():
            print("✅ Los datos iniciales ya existen")
            return
        
        print("📦 Cargando datos iniciales...")
        
        # Crear categorías
        cat1 = Categoria.objects.create(
            nombre='Electrónicos',
            descripcion='Productos electrónicos y tecnológicos'
        )
        cat2 = Categoria.objects.create(
            nombre='Hogar',
            descripcion='Productos para el hogar y cocina'
        )
        cat3 = Categoria.objects.create(
            nombre='Oficina',
            descripcion='Productos de oficina y papelería'
        )
        
        # Crear proveedores
        prov1 = Proveedor.objects.create(
            nombre='TechSupply',
            telefono='555-0001',
            email='ventas@techsupply.com',
            direccion='Av. Tecnología 123, Ciudad'
        )
        prov2 = Proveedor.objects.create(
            nombre='HomeGoods',
            telefono='555-0002',
            email='info@homegoods.com',
            direccion='Calle Hogar 456, Ciudad'
        )
        
        # Crear productos
        Producto.objects.create(
            nombre='Laptop Dell Inspiron',
            descripcion='Laptop Dell Inspiron 15, 8GB RAM, 256GB SSD',
            precio=15000.00,
            stock=10,
            stock_minimo=2,
            categoria=cat1,
            proveedor=prov1
        )
        
        Producto.objects.create(
            nombre='Mouse Inalámbrico',
            descripcion='Mouse inalámbrico ergonómico con receptor USB',
            precio=350.00,
            stock=25,
            stock_minimo=5,
            categoria=cat1,
            proveedor=prov1
        )
        
        Producto.objects.create(
            nombre='Cafetera Automática',
            descripcion='Cafetera automática programable 12 tazas',
            precio=2500.00,
            stock=8,
            stock_minimo=3,
            categoria=cat2,
            proveedor=prov2
        )
        
        # Crear usuario operador de ejemplo
        Usuario.objects.create_user(
            username='operador',
            email='operador@inventario.com',
            password='operador123',
            first_name='Juan',
            last_name='Pérez',
            rol='operador'
        )
        
        print("✅ Datos iniciales cargados exitosamente:")
        print(f"   Categorías: {Categoria.objects.count()}")
        print(f"   Proveedores: {Proveedor.objects.count()}")
        print(f"   Productos: {Producto.objects.count()}")
        print(f"   Usuarios: {Usuario.objects.count()}")
        
    except Exception as e:
        print(f"❌ Error cargando datos iniciales: {e}")

if __name__ == '__main__':
    load_initial_data()