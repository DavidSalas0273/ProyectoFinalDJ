from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Producto
from .forms import ProductoForm
from core.decorators import solo_admin


@login_required(login_url='login')
def lista_productos(request):
    """Todos los usuarios autenticados pueden ver la lista."""
    productos = Producto.objects.select_related('categoria', 'proveedor').all()
    return render(request, 'productos/lista.html', {'productos': productos})


@login_required(login_url='login')
def crear_producto(request):
    """Solo admins pueden crear productos."""
    if not request.user.es_admin():
        messages.error(request, 'Solo los administradores pueden crear productos.')
        return redirect('lista_productos')

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/crear.html', {'form': form})


@login_required(login_url='login')
def editar_producto(request, id):
    """Solo admins pueden editar productos."""
    if not request.user.es_admin():
        messages.error(request, 'Solo los administradores pueden editar productos.')
        return redirect('lista_productos')

    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar.html', {'form': form})


@login_required(login_url='login')
@solo_admin
def eliminar_producto(request, id):
    """Solo admins pueden eliminar productos."""
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('lista_productos')

    return render(request, 'productos/eliminar.html', {'producto': producto})
