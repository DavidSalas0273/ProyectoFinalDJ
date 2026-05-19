import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Producto, Categoria, Proveedor, Compra, Venta


# ─────────────────────────────────────────────
# Mixin reutilizable: trim + validación de solo espacios
# ─────────────────────────────────────────────

class TrimMixin:
    """
    Elimina espacios al inicio y al final de todos los CharField/EmailField.
    Rechaza campos requeridos que queden vacíos tras el trim.
    """
    def clean(self):
        cleaned = super().clean()
        for field_name, value in cleaned.items():
            if isinstance(value, str):
                stripped = value.strip()
                if stripped != value:
                    cleaned[field_name] = stripped
                if not stripped and self.fields.get(field_name) and self.fields[field_name].required:
                    self.add_error(field_name, 'Este campo no puede contener solo espacios.')
        return cleaned


# ─────────────────────────────────────────────
# Producto
# ─────────────────────────────────────────────

class ProductoForm(TrimMixin, forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'stock_minimo', 'categoria', 'proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Nombre del producto',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': '500',
                'placeholder': 'Descripción breve (máx. 500 caracteres)',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio': 'Precio',
            'stock': 'Stock actual',
            'stock_minimo': 'Stock mínimo (alerta)',
            'categoria': 'Categoría',
            'proveedor': 'Proveedor',
        }

    def clean_nombre(self):
        value = self.cleaned_data.get('nombre', '').strip()
        if not value:
            raise ValidationError('El nombre no puede estar vacío ni contener solo espacios.')
        if len(value) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        if len(value) > 100:
            raise ValidationError('El nombre no puede superar los 100 caracteres.')
        return value

    def clean_descripcion(self):
        value = self.cleaned_data.get('descripcion', '').strip()
        if len(value) > 500:
            raise ValidationError('La descripción no puede superar los 500 caracteres.')
        return value

    def clean_precio(self):
        value = self.cleaned_data.get('precio')
        if value is None:
            raise ValidationError('El precio es obligatorio.')
        if value <= 0:
            raise ValidationError('El precio debe ser mayor a 0.')
        if value > 9_999_999.99:
            raise ValidationError('El precio no puede superar $9,999,999.99.')
        return value

    def clean_stock(self):
        value = self.cleaned_data.get('stock')
        if value is None:
            raise ValidationError('El stock es obligatorio.')
        if value < 0:
            raise ValidationError('El stock no puede ser negativo.')
        if value > 999_999:
            raise ValidationError('El stock no puede superar 999,999 unidades.')
        return value

    def clean_stock_minimo(self):
        value = self.cleaned_data.get('stock_minimo')
        if value is None:
            raise ValidationError('El stock mínimo es obligatorio.')
        if value < 0:
            raise ValidationError('El stock mínimo no puede ser negativo.')
        return value

    def clean(self):
        cleaned = super().clean()
        stock = cleaned.get('stock')
        stock_minimo = cleaned.get('stock_minimo')
        if stock is not None and stock_minimo is not None:
            if stock_minimo > stock:
                self.add_error(
                    'stock_minimo',
                    'El stock mínimo no puede ser mayor al stock actual.',
                )
        return cleaned


# ─────────────────────────────────────────────
# Categoría
# ─────────────────────────────────────────────

class CategoriaForm(TrimMixin, forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Nombre de la categoría',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': '300',
                'placeholder': 'Descripción (máx. 300 caracteres)',
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
        }

    def clean_nombre(self):
        value = self.cleaned_data.get('nombre', '').strip()
        if not value:
            raise ValidationError('El nombre no puede estar vacío ni contener solo espacios.')
        if len(value) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        if len(value) > 100:
            raise ValidationError('El nombre no puede superar los 100 caracteres.')
        # Verificar duplicados (case-insensitive), excluyendo la instancia actual
        qs = Categoria.objects.filter(nombre__iexact=value)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe una categoría con ese nombre.')
        return value

    def clean_descripcion(self):
        value = self.cleaned_data.get('descripcion', '').strip()
        if len(value) > 300:
            raise ValidationError('La descripción no puede superar los 300 caracteres.')
        return value


# ─────────────────────────────────────────────
# Proveedor
# ─────────────────────────────────────────────

class ProveedorForm(TrimMixin, forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '100',
                'placeholder': 'Nombre del proveedor',
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '20',
                'placeholder': 'Ej: +52 55 1234 5678',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'maxlength': '150',
                'placeholder': 'correo@proveedor.com',
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '200',
                'placeholder': 'Dirección completa',
            }),
        }
        labels = {
            'nombre': 'Nombre',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'direccion': 'Dirección',
        }

    def clean_nombre(self):
        value = self.cleaned_data.get('nombre', '').strip()
        if not value:
            raise ValidationError('El nombre no puede estar vacío ni contener solo espacios.')
        if len(value) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        if len(value) > 100:
            raise ValidationError('El nombre no puede superar los 100 caracteres.')
        return value

    def clean_telefono(self):
        value = self.cleaned_data.get('telefono', '').strip()
        if not value:
            raise ValidationError('El teléfono es obligatorio.')
        # Permite dígitos, espacios, +, -, paréntesis
        if not re.match(r'^[\d\s\+\-\(\)]{7,20}$', value):
            raise ValidationError('Teléfono inválido. Usa solo dígitos, espacios, +, - o paréntesis (7-20 caracteres).')
        return value

    def clean_email(self):
        value = self.cleaned_data.get('email', '').strip().lower()
        if not value:
            raise ValidationError('El correo es obligatorio.')
        # Verificar duplicados excluyendo la instancia actual
        qs = Proveedor.objects.filter(email=value)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un proveedor con este correo.')
        return value

    def clean_direccion(self):
        value = self.cleaned_data.get('direccion', '').strip()
        if len(value) > 200:
            raise ValidationError('La dirección no puede superar los 200 caracteres.')
        return value


# ─────────────────────────────────────────────
# Compra
# ─────────────────────────────────────────────

class CompraForm(TrimMixin, forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['producto', 'proveedor', 'cantidad', 'precio_unitario', 'notas']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '999999',
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'maxlength': '300',
                'placeholder': 'Notas adicionales (opcional, máx. 300 caracteres)',
            }),
        }
        labels = {
            'producto': 'Producto',
            'proveedor': 'Proveedor',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario',
            'notas': 'Notas',
        }

    def clean_cantidad(self):
        value = self.cleaned_data.get('cantidad')
        if value is None:
            raise ValidationError('La cantidad es obligatoria.')
        if value <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')
        if value > 999_999:
            raise ValidationError('La cantidad no puede superar 999,999 unidades.')
        return value

    def clean_precio_unitario(self):
        value = self.cleaned_data.get('precio_unitario')
        if value is None:
            raise ValidationError('El precio unitario es obligatorio.')
        if value <= 0:
            raise ValidationError('El precio unitario debe ser mayor a 0.')
        if value > 9_999_999.99:
            raise ValidationError('El precio no puede superar $9,999,999.99.')
        return value

    def clean_notas(self):
        value = self.cleaned_data.get('notas', '').strip()
        if len(value) > 300:
            raise ValidationError('Las notas no pueden superar los 300 caracteres.')
        return value


# ─────────────────────────────────────────────
# Venta
# ─────────────────────────────────────────────

class VentaForm(TrimMixin, forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'precio_unitario', 'notas']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '999999',
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'maxlength': '300',
                'placeholder': 'Notas adicionales (opcional, máx. 300 caracteres)',
            }),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario',
            'notas': 'Notas',
        }

    def clean_cantidad(self):
        value = self.cleaned_data.get('cantidad')
        if value is None:
            raise ValidationError('La cantidad es obligatoria.')
        if value <= 0:
            raise ValidationError('La cantidad debe ser mayor a 0.')
        if value > 999_999:
            raise ValidationError('La cantidad no puede superar 999,999 unidades.')
        return value

    def clean_precio_unitario(self):
        value = self.cleaned_data.get('precio_unitario')
        if value is None:
            raise ValidationError('El precio unitario es obligatorio.')
        if value <= 0:
            raise ValidationError('El precio unitario debe ser mayor a 0.')
        if value > 9_999_999.99:
            raise ValidationError('El precio no puede superar $9,999,999.99.')
        return value

    def clean_notas(self):
        value = self.cleaned_data.get('notas', '').strip()
        if len(value) > 300:
            raise ValidationError('Las notas no pueden superar los 300 caracteres.')
        return value

    def clean(self):
        cleaned = super().clean()
        producto = cleaned.get('producto')
        cantidad = cleaned.get('cantidad')
        if producto and cantidad:
            if cantidad > producto.stock:
                self.add_error(
                    'cantidad',
                    f'Stock insuficiente. Disponible: {producto.stock} unidades.',
                )
        return cleaned


# ─────────────────────────────────────────────
# Filtro de reportes
# ─────────────────────────────────────────────

class FiltroReporteForm(forms.Form):
    """Formulario de filtros para reportes y dashboard."""

    fecha_inicio = forms.DateField(
        required=False,
        label='Fecha inicio',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    fecha_fin = forms.DateField(
        required=False,
        label='Fecha fin',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label='Todas las categorías',
        label='Categoría',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        required=False,
        empty_label='Todos los proveedores',
        label='Proveedor',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    def clean(self):
        cleaned = super().clean()
        fecha_inicio = cleaned.get('fecha_inicio')
        fecha_fin = cleaned.get('fecha_fin')
        if fecha_inicio and fecha_fin and fecha_inicio > fecha_fin:
            raise ValidationError('La fecha de inicio no puede ser posterior a la fecha fin.')
        return cleaned
