from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistroUsuarioForm, LoginForm, PerfilUsuarioForm


def registro(request):
    """Vista para registrar un nuevo usuario (rol operador por defecto)."""
    if request.user.is_authenticated:
        return _redirigir_por_rol(request.user)

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name}! Tu cuenta ha sido creada.')
            return _redirigir_por_rol(user)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'auth/registro.html', {'form': form})


def iniciar_sesion(request):
    """Vista de login personalizada. Redirige según rol."""
    if request.user.is_authenticated:
        return _redirigir_por_rol(request.user)

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            # Si hay un ?next= explícito lo respetamos, si no redirigimos por rol
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return _redirigir_por_rol(user)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form})


def _redirigir_por_rol(user):
    """Devuelve un redirect según el rol del usuario."""
    if user.es_admin():
        return redirect('dashboard')
    return redirect('dashboard_operador')


def cerrar_sesion(request):
    """Vista de logout."""
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'Has cerrado sesión correctamente.')
        return redirect('login')
    return render(request, 'auth/logout_confirm.html')


@login_required(login_url='login')
def perfil(request):
    """Vista del perfil del usuario autenticado."""
    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = PerfilUsuarioForm(instance=request.user)

    return render(request, 'auth/perfil.html', {'form': form})


@login_required(login_url='login')
def dashboard_operador(request):
    """Dashboard exclusivo para operadores: solo ve ventas y productos."""
    from gestion_inventario.models import Producto, Venta
    from django.db.models import Sum, F

    # Si un admin llega aquí lo mandamos a su dashboard
    if request.user.es_admin():
        return redirect('dashboard')

    productos = Producto.objects.select_related('categoria', 'proveedor').all()
    productos_bajo_stock = [p for p in productos if p.bajo_stock]

    mis_ventas = Venta.objects.filter(usuario=request.user).select_related('producto').order_by('-fecha')[:10]
    total_mis_ventas = Venta.objects.filter(usuario=request.user).aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )['total'] or 0

    return render(request, 'dashboard/operador.html', {
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock,
        'mis_ventas': mis_ventas,
        'total_mis_ventas': total_mis_ventas,
    })
