from django.contrib import admin
from .models import Categoria, Proveedor, Producto, MovimientoInventario, Compra, Venta


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'direccion')
    search_fields = ('nombre', 'email')


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'proveedor', 'precio', 'stock', 'stock_minimo', 'bajo_stock')
    list_filter = ('categoria', 'proveedor')
    search_fields = ('nombre',)

    @admin.display(boolean=True, description='Bajo stock')
    def bajo_stock(self, obj):
        return obj.bajo_stock


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'tipo', 'cantidad', 'fecha', 'usuario')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre',)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'proveedor', 'cantidad', 'precio_unitario', 'fecha', 'usuario')
    list_filter = ('proveedor', 'fecha')
    search_fields = ('producto__nombre',)


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'precio_unitario', 'fecha', 'usuario')
    list_filter = ('fecha',)
    search_fields = ('producto__nombre',)
