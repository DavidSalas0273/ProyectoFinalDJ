#!/usr/bin/env bash
# build.sh — Script de build para Render
set -o errexit   # salir si cualquier comando falla

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "👤 Creando superusuario..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
django.setup()
from core.models import Usuario
try:
    if not Usuario.objects.filter(is_superuser=True).exists():
        Usuario.objects.create_superuser(
            username='admin',
            email='admin@inventario.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            rol='admin'
        )
        print('✅ Superusuario creado')
    else:
        print('✅ Superusuario ya existe')
except Exception as e:
    print(f'⚠️ Error creando superusuario: {e}')
"

echo "📦 Cargando datos iniciales..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventario.settings')
django.setup()
from gestion_inventario.models import Categoria, Proveedor, Producto
from core.models import Usuario
try:
    if not Categoria.objects.exists():
        # Crear categorías
        cat1 = Categoria.objects.create(nombre='Electrónicos', descripcion='Productos electrónicos')
        cat2 = Categoria.objects.create(nombre='Hogar', descripcion='Productos para el hogar')
        # Crear proveedores
        prov1 = Proveedor.objects.create(nombre='TechSupply', telefono='555-0001', email='ventas@techsupply.com', direccion='Av. Tecnología 123')
        # Crear productos
        Producto.objects.create(nombre='Laptop Dell', descripcion='Laptop Dell Inspiron 15', precio=15000.00, stock=10, stock_minimo=2, categoria=cat1, proveedor=prov1)
        # Crear operador
        if not Usuario.objects.filter(username='operador').exists():
            Usuario.objects.create_user(username='operador', email='operador@inventario.com', password='operador123', first_name='Juan', last_name='Pérez', rol='operador')
        print('✅ Datos iniciales cargados')
    else:
        print('✅ Datos iniciales ya existen')
except Exception as e:
    print(f'⚠️ Error cargando datos: {e}')
"

echo "🔍 Verificando configuración..."
python debug_settings.py

echo "✅ Build completado exitosamente"
