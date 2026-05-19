from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegistroUsuarioForm, LoginForm, PerfilUsuarioForm


def registro(request):
    """Vista para registrar un nuevo usuario (rol operador por defecto)."""
    if request.user.is_authenticated:
        return redirect('lista_productos')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Bienvenido, {user.first_name}! Tu cuenta ha sido creada.')
            return redirect('lista_productos')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'auth/registro.html', {'form': form})


def iniciar_sesion(request):
    """Vista de login personalizada."""
    if request.user.is_authenticated:
        return redirect('lista_productos')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Bienvenido de nuevo, {user.first_name or user.username}!')
            # Redirigir a la URL solicitada originalmente o al inicio
            next_url = request.GET.get('next', 'lista_productos')
            return redirect(next_url)
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm(request)

    return render(request, 'auth/login.html', {'form': form})


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
