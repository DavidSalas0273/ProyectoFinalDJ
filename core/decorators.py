from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def solo_admin(view_func):
    """Permite el acceso solo a usuarios con rol admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.es_admin:
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('dashboard_operador')
        return view_func(request, *args, **kwargs)
    return wrapper


def solo_operador(view_func):
    """Permite el acceso solo a usuarios con rol operador."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.es_operador:
            messages.error(request, 'Esta sección es solo para operadores.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def login_requerido(view_func):
    """Redirige al login si el usuario no está autenticado."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Debes iniciar sesión para continuar.')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
