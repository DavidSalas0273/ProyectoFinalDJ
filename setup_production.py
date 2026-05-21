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

            # ── Categorías ──────────────────────────────────────────
            cat_elec  = Categoria.objects.create(nombre='Electrónicos',   descripcion='Computadoras, celulares y accesorios tecnológicos')
            cat_hogar = Categoria.objects.create(nombre='Hogar',          descripcion='Electrodomésticos y artículos para el hogar')
            cat_ofic  = Categoria.objects.create(nombre='Oficina',        descripcion='Papelería, mobiliario y suministros de oficina')
            cat_ropa  = Categoria.objects.create(nombre='Ropa',           descripcion='Prendas de vestir y accesorios de moda')
            cat_depo  = Categoria.objects.create(nombre='Deportes',       descripcion='Equipos y ropa deportiva')
            cat_alim  = Categoria.objects.create(nombre='Alimentos',      descripcion='Productos alimenticios y bebidas')

            # ── Proveedores ─────────────────────────────────────────
            prov_tech  = Proveedor.objects.create(nombre='TechSupply',       telefono='555-1001', email='ventas@techsupply.com',      direccion='Av. Tecnología 123, CDMX')
            prov_home  = Proveedor.objects.create(nombre='HomeGoods',        telefono='555-1002', email='contacto@homegoods.com',      direccion='Calle Hogar 456, Guadalajara')
            prov_off   = Proveedor.objects.create(nombre='OfficeMax',        telefono='555-1003', email='pedidos@officemax.com',       direccion='Blvd. Oficina 789, Monterrey')
            prov_moda  = Proveedor.objects.create(nombre='ModaExpress',      telefono='555-1004', email='ventas@modaexpress.com',      direccion='Paseo de la Moda 321, Puebla')
            prov_depo  = Proveedor.objects.create(nombre='SportZone',        telefono='555-1005', email='info@sportzone.com',          direccion='Av. Deporte 654, Monterrey')
            prov_dist  = Proveedor.objects.create(nombre='Distribuidora MX', telefono='555-1006', email='distribuidora@mx.com',        direccion='Calle Comercio 987, CDMX')

            # ── Productos ───────────────────────────────────────────
            productos = [
                # Electrónicos
                dict(nombre='Laptop Dell Inspiron 15',    descripcion='Laptop 15", Intel Core i5, 8GB RAM, 256GB SSD',          precio=14999.00, stock=12, stock_minimo=3, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Laptop HP Pavilion',         descripcion='Laptop 14", AMD Ryzen 5, 16GB RAM, 512GB SSD',           precio=13500.00, stock=8,  stock_minimo=2, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Monitor LG 24"',             descripcion='Monitor Full HD IPS 24 pulgadas, 75Hz',                  precio=3800.00,  stock=15, stock_minimo=4, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Teclado Mecánico Logitech',  descripcion='Teclado mecánico inalámbrico, switches azules',          precio=1200.00,  stock=20, stock_minimo=5, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Mouse Inalámbrico',          descripcion='Mouse ergonómico inalámbrico con receptor USB',          precio=350.00,   stock=30, stock_minimo=8, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Audífonos Sony WH-1000XM4',  descripcion='Audífonos over-ear con cancelación de ruido',           precio=5500.00,  stock=10, stock_minimo=2, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Tablet Samsung Galaxy A8',   descripcion='Tablet 10.5", 4GB RAM, 64GB almacenamiento',            precio=6200.00,  stock=7,  stock_minimo=2, categoria=cat_elec,  proveedor=prov_tech),
                dict(nombre='Cámara Web Logitech C920',   descripcion='Webcam Full HD 1080p con micrófono integrado',          precio=1800.00,  stock=18, stock_minimo=4, categoria=cat_elec,  proveedor=prov_tech),

                # Hogar
                dict(nombre='Cafetera Automática',        descripcion='Cafetera programable 12 tazas con temporizador',        precio=2500.00,  stock=9,  stock_minimo=2, categoria=cat_hogar, proveedor=prov_home),
                dict(nombre='Licuadora Oster 10 vel.',    descripcion='Licuadora de 10 velocidades, vaso de vidrio 1.5L',      precio=1100.00,  stock=14, stock_minimo=3, categoria=cat_hogar, proveedor=prov_home),
                dict(nombre='Microondas Panasonic 1.1ft', descripcion='Microondas 1100W con cocción inversa',                  precio=3200.00,  stock=6,  stock_minimo=2, categoria=cat_hogar, proveedor=prov_home),
                dict(nombre='Aspiradora Dyson V11',       descripcion='Aspiradora inalámbrica de alta potencia',               precio=9800.00,  stock=5,  stock_minimo=1, categoria=cat_hogar, proveedor=prov_home),
                dict(nombre='Plancha de Vapor Philips',   descripcion='Plancha de vapor 2400W con suela de cerámica',          precio=850.00,   stock=20, stock_minimo=5, categoria=cat_hogar, proveedor=prov_home),
                dict(nombre='Ventilador de Torre',        descripcion='Ventilador de torre 40" con control remoto',            precio=1400.00,  stock=11, stock_minimo=3, categoria=cat_hogar, proveedor=prov_home),

                # Oficina
                dict(nombre='Silla Ergonómica',           descripcion='Silla de oficina con soporte lumbar ajustable',         precio=4500.00,  stock=8,  stock_minimo=2, categoria=cat_ofic,  proveedor=prov_off),
                dict(nombre='Escritorio de Madera',       descripcion='Escritorio 120x60cm con cajón y estante',               precio=3200.00,  stock=5,  stock_minimo=1, categoria=cat_ofic,  proveedor=prov_off),
                dict(nombre='Resma de Papel Carta',       descripcion='Resma 500 hojas papel bond 75g/m²',                    precio=120.00,   stock=80, stock_minimo=20, categoria=cat_ofic,  proveedor=prov_off),
                dict(nombre='Impresora HP LaserJet',      descripcion='Impresora láser monocromática, 30ppm',                  precio=4200.00,  stock=7,  stock_minimo=2, categoria=cat_ofic,  proveedor=prov_off),
                dict(nombre='Cartucho de Tinta HP 664',   descripcion='Cartucho de tinta negra original HP 664',              precio=280.00,   stock=40, stock_minimo=10, categoria=cat_ofic,  proveedor=prov_off),
                dict(nombre='Archivero Metálico 4 gav.',  descripcion='Archivero metálico de 4 gavetas con llave',             precio=2800.00,  stock=4,  stock_minimo=1, categoria=cat_ofic,  proveedor=prov_off),

                # Ropa
                dict(nombre='Playera Polo Hombre',        descripcion='Playera polo 100% algodón, tallas S-XXL',              precio=320.00,   stock=50, stock_minimo=10, categoria=cat_ropa,  proveedor=prov_moda),
                dict(nombre='Jeans Slim Fit',             descripcion='Pantalón de mezclilla slim fit, varios colores',        precio=580.00,   stock=35, stock_minimo=8,  categoria=cat_ropa,  proveedor=prov_moda),
                dict(nombre='Chamarra de Cuero',          descripcion='Chamarra de cuero sintético, forro polar',              precio=1200.00,  stock=15, stock_minimo=3,  categoria=cat_ropa,  proveedor=prov_moda),
                dict(nombre='Vestido Casual Mujer',       descripcion='Vestido casual floral, telas ligeras, tallas XS-XL',   precio=450.00,   stock=25, stock_minimo=5,  categoria=cat_ropa,  proveedor=prov_moda),
                dict(nombre='Tenis Nike Air Max',         descripcion='Tenis deportivos con amortiguación Air Max',            precio=2200.00,  stock=20, stock_minimo=4,  categoria=cat_ropa,  proveedor=prov_moda),

                # Deportes
                dict(nombre='Bicicleta de Montaña',       descripcion='Bicicleta MTB rodada 26, 21 velocidades',              precio=5800.00,  stock=6,  stock_minimo=1,  categoria=cat_depo,  proveedor=prov_depo),
                dict(nombre='Pesas Hexagonales 10kg',     descripcion='Par de mancuernas hexagonales de 10kg',                precio=680.00,   stock=18, stock_minimo=4,  categoria=cat_depo,  proveedor=prov_depo),
                dict(nombre='Colchoneta de Yoga',         descripcion='Colchoneta antideslizante 6mm, varios colores',        precio=350.00,   stock=25, stock_minimo=6,  categoria=cat_depo,  proveedor=prov_depo),
                dict(nombre='Cuerda para Saltar',         descripcion='Cuerda de saltar con mangos ergonómicos',              precio=120.00,   stock=40, stock_minimo=10, categoria=cat_depo,  proveedor=prov_depo),
                dict(nombre='Balón de Fútbol Nike',       descripcion='Balón de fútbol talla 5, cosido a mano',               precio=480.00,   stock=22, stock_minimo=5,  categoria=cat_depo,  proveedor=prov_depo),

                # Alimentos
                dict(nombre='Café Molido 500g',           descripcion='Café molido de altura, tostado medio, 500g',           precio=180.00,   stock=60, stock_minimo=15, categoria=cat_alim,  proveedor=prov_dist),
                dict(nombre='Aceite de Oliva 1L',         descripcion='Aceite de oliva extra virgen, primera extracción',     precio=220.00,   stock=45, stock_minimo=10, categoria=cat_alim,  proveedor=prov_dist),
                dict(nombre='Avena Quaker 1kg',           descripcion='Avena en hojuelas tradicional, 1 kilogramo',           precio=85.00,    stock=70, stock_minimo=20, categoria=cat_alim,  proveedor=prov_dist),
                dict(nombre='Agua Mineral 24 pack',       descripcion='Caja de 24 botellas de agua mineral 600ml',            precio=160.00,   stock=50, stock_minimo=12, categoria=cat_alim,  proveedor=prov_dist),
            ]

            for p in productos:
                Producto.objects.create(**p)

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