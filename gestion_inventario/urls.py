from django.urls import path
from . import views

urlpatterns = [
    # Productos
    path('', views.lista_productos, name='lista_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),

    # Categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/crear/', views.crear_categoria, name='crear_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:id>/', views.eliminar_categoria, name='eliminar_categoria'),

    # Proveedores
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),

    # Compras
    path('compras/', views.lista_compras, name='lista_compras'),
    path('compras/crear/', views.crear_compra, name='crear_compra'),

    # Ventas
    path('ventas/', views.lista_ventas, name='lista_ventas'),
    path('ventas/crear/', views.crear_venta, name='crear_venta'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Reportes
    path('reportes/inventario/', views.reporte_inventario, name='reporte_inventario'),
    path('reportes/ventas/', views.reporte_ventas, name='reporte_ventas'),
    path('reportes/inventario/excel/', views.exportar_inventario_excel, name='exportar_inventario_excel'),
    path('reportes/ventas/excel/', views.exportar_ventas_excel, name='exportar_ventas_excel'),
]
