from django.db import models
from django.conf import settings


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    telefono = models.CharField(max_length=20, verbose_name='Teléfono')
    email = models.EmailField(verbose_name='Correo electrónico')
    direccion = models.CharField(max_length=200, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre']


class Producto(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.IntegerField(default=0, verbose_name='Stock actual')
    stock_minimo = models.IntegerField(default=5, verbose_name='Stock mínimo')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name='Categoría')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')

    def __str__(self):
        return self.nombre

    @property
    def bajo_stock(self):
        """Retorna True si el stock está por debajo del mínimo."""
        return self.stock <= self.stock_minimo

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']


class MovimientoInventario(models.Model):

    TIPOS = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    tipo = models.CharField(max_length=10, choices=TIPOS, verbose_name='Tipo')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario',
    )

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} ({self.cantidad})"

    class Meta:
        verbose_name = 'Movimiento de inventario'
        verbose_name_plural = 'Movimientos de inventario'
        ordering = ['-fecha']


class Compra(models.Model):
    """Registro de compras a proveedores. Incrementa el stock automáticamente."""

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio unitario')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario',
    )
    notas = models.TextField(blank=True, verbose_name='Notas')

    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        """Al guardar una compra nueva, incrementa el stock del producto."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.producto.stock += self.cantidad
            self.producto.save()
            MovimientoInventario.objects.create(
                producto=self.producto,
                tipo='entrada',
                cantidad=self.cantidad,
                usuario=self.usuario,
            )

    def __str__(self):
        return f"Compra {self.id} - {self.producto.nombre} ({self.cantidad})"

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-fecha']


class Venta(models.Model):
    """Registro de ventas. Decrementa el stock automáticamente."""

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField(verbose_name='Cantidad')
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio unitario')
    fecha = models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuario',
    )
    notas = models.TextField(blank=True, verbose_name='Notas')

    @property
    def total(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        """Al guardar una venta nueva, decrementa el stock del producto."""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.producto.stock -= self.cantidad
            self.producto.save()
            MovimientoInventario.objects.create(
                producto=self.producto,
                tipo='salida',
                cantidad=self.cantidad,
                usuario=self.usuario,
            )

    def __str__(self):
        return f"Venta {self.id} - {self.producto.nombre} ({self.cantidad})"

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        ordering = ['-fecha']