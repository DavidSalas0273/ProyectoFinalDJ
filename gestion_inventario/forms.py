from django import forms
from .models import Producto, Categoria, Proveedor, Compra, Venta


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'stock_minimo', 'categoria', 'proveedor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
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


class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
        }


class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor
        fields = ['nombre', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'direccion': 'Dirección',
        }


class CompraForm(forms.ModelForm):

    class Meta:
        model = Compra
        fields = ['producto', 'proveedor', 'cantidad', 'precio_unitario', 'notas']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'producto': 'Producto',
            'proveedor': 'Proveedor',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario',
            'notas': 'Notas',
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is not None and cantidad <= 0:
            raise forms.ValidationError('La cantidad debe ser mayor a 0.')
        return cantidad


class VentaForm(forms.ModelForm):

    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'precio_unitario', 'notas']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_unitario': 'Precio unitario',
            'notas': 'Notas',
        }

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        if producto and cantidad:
            if cantidad <= 0:
                self.add_error('cantidad', 'La cantidad debe ser mayor a 0.')
            elif cantidad > producto.stock:
                self.add_error(
                    'cantidad',
                    f'Stock insuficiente. Disponible: {producto.stock} unidades.',
                )
        return cleaned_data


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
