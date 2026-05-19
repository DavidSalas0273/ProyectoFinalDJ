import json
import io
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse

from .models import Producto, Categoria, Proveedor, Compra, Venta, MovimientoInventario
from .forms import (
    ProductoForm, CategoriaForm, ProveedorForm,
    CompraForm, VentaForm, FiltroReporteForm,
)
from core.decorators import solo_admin


# ─────────────────────────────────────────────
# PRODUCTOS
# ─────────────────────────────────────────────

@login_required(login_url='login')
def lista_productos(request):
    """Todos los usuarios autenticados pueden ver la lista."""
    productos = Producto.objects.select_related('categoria', 'proveedor').all()
    productos_bajo_stock = [p for p in productos if p.bajo_stock]
    return render(request, 'productos/lista.html', {
        'productos': productos,
        'productos_bajo_stock': productos_bajo_stock,
    })


@login_required(login_url='login')
@solo_admin
def crear_producto(request):
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
@solo_admin
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/editar.html', {'form': form, 'producto': producto})


@login_required(login_url='login')
@solo_admin
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('lista_productos')
    return render(request, 'productos/eliminar.html', {'producto': producto})


# ─────────────────────────────────────────────
# CATEGORÍAS
# ─────────────────────────────────────────────

@login_required(login_url='login')
def lista_categorias(request):
    categorias = Categoria.objects.annotate(total_productos=Count('producto')).all()
    return render(request, 'categorias/lista.html', {'categorias': categorias})


@login_required(login_url='login')
@solo_admin
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm()
    return render(request, 'categorias/crear.html', {'form': form})


@login_required(login_url='login')
@solo_admin
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('lista_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'categorias/editar.html', {'form': form, 'categoria': categoria})


@login_required(login_url='login')
@solo_admin
def eliminar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada correctamente.')
        return redirect('lista_categorias')
    return render(request, 'categorias/eliminar.html', {'categoria': categoria})


# ─────────────────────────────────────────────
# PROVEEDORES
# ─────────────────────────────────────────────

@login_required(login_url='login')
def lista_proveedores(request):
    proveedores = Proveedor.objects.annotate(total_productos=Count('producto')).all()
    return render(request, 'proveedores/lista.html', {'proveedores': proveedores})


@login_required(login_url='login')
@solo_admin
def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/crear.html', {'form': form})


@login_required(login_url='login')
@solo_admin
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedores/editar.html', {'form': form, 'proveedor': proveedor})


@login_required(login_url='login')
@solo_admin
def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado correctamente.')
        return redirect('lista_proveedores')
    return render(request, 'proveedores/eliminar.html', {'proveedor': proveedor})


# ─────────────────────────────────────────────
# COMPRAS
# ─────────────────────────────────────────────

@login_required(login_url='login')
def lista_compras(request):
    compras = Compra.objects.select_related('producto', 'proveedor', 'usuario').all()
    return render(request, 'compras/lista.html', {'compras': compras})


@login_required(login_url='login')
@solo_admin
def crear_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user
            compra.save()
            messages.success(
                request,
                f'Compra registrada. Stock de "{compra.producto.nombre}" actualizado a {compra.producto.stock}.',
            )
            return redirect('lista_compras')
    else:
        form = CompraForm()
    return render(request, 'compras/crear.html', {'form': form})


# ─────────────────────────────────────────────
# VENTAS
# ─────────────────────────────────────────────

@login_required(login_url='login')
def lista_ventas(request):
    ventas = Venta.objects.select_related('producto', 'usuario').all()
    return render(request, 'ventas/lista.html', {'ventas': ventas})


@login_required(login_url='login')
def crear_venta(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.save()
            messages.success(
                request,
                f'Venta registrada. Stock de "{venta.producto.nombre}" actualizado a {venta.producto.stock}.',
            )
            if venta.producto.bajo_stock:
                messages.warning(
                    request,
                    f'Alerta: "{venta.producto.nombre}" tiene stock bajo ({venta.producto.stock} unidades).',
                )
            return redirect('lista_ventas')
    else:
        form = VentaForm()
    return render(request, 'ventas/crear.html', {'form': form})


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@login_required(login_url='login')
@solo_admin
def dashboard(request):
    """Dashboard principal con métricas, gráficos y alertas."""

    # ── Métricas generales ──────────────────────────────────────────
    total_productos = Producto.objects.count()
    total_categorias = Categoria.objects.count()
    total_proveedores = Proveedor.objects.count()

    total_ventas = Venta.objects.aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )['total'] or 0

    total_compras = Compra.objects.aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )['total'] or 0

    productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'))

    # ── Gráfico 1: Productos más vendidos (top 10) ──────────────────
    top_vendidos = (
        Venta.objects.values('producto__nombre')
        .annotate(total_vendido=Sum('cantidad'))
        .order_by('-total_vendido')[:10]
    )
    labels_ventas = json.dumps([v['producto__nombre'] for v in top_vendidos])
    data_ventas = json.dumps([v['total_vendido'] for v in top_vendidos])

    # ── Gráfico 2: Stock por categoría ─────────────────────────────
    stock_por_categoria = (
        Producto.objects.values('categoria__nombre')
        .annotate(total_stock=Sum('stock'))
        .order_by('categoria__nombre')
    )
    labels_categorias = json.dumps([s['categoria__nombre'] for s in stock_por_categoria])
    data_stock = json.dumps([s['total_stock'] for s in stock_por_categoria])

    # ── Gráfico 3: Ventas últimos 30 días ──────────────────────────
    hace_30_dias = date.today() - timedelta(days=30)
    ventas_diarias = (
        Venta.objects.filter(fecha__date__gte=hace_30_dias)
        .annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(total=Sum('cantidad'))
        .order_by('dia')
    )
    labels_dias = json.dumps([str(v['dia']) for v in ventas_diarias])
    data_dias = json.dumps([v['total'] for v in ventas_diarias])

    context = {
        'total_productos': total_productos,
        'total_categorias': total_categorias,
        'total_proveedores': total_proveedores,
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        'productos_bajo_stock': productos_bajo_stock,
        'labels_ventas': labels_ventas,
        'data_ventas': data_ventas,
        'labels_categorias': labels_categorias,
        'data_stock': data_stock,
        'labels_dias': labels_dias,
        'data_dias': data_dias,
    }
    return render(request, 'dashboard/index.html', context)


# ─────────────────────────────────────────────
# REPORTES
# ─────────────────────────────────────────────

@login_required(login_url='login')
@solo_admin
def reporte_inventario(request):
    """Reporte de inventario con filtros."""
    form = FiltroReporteForm(request.GET or None)
    productos = Producto.objects.select_related('categoria', 'proveedor').all()

    if form.is_valid():
        categoria = form.cleaned_data.get('categoria')
        proveedor = form.cleaned_data.get('proveedor')
        if categoria:
            productos = productos.filter(categoria=categoria)
        if proveedor:
            productos = productos.filter(proveedor=proveedor)

    return render(request, 'reportes/inventario.html', {
        'form': form,
        'productos': productos,
    })


@login_required(login_url='login')
@solo_admin
def reporte_ventas(request):
    """Reporte de ventas con filtros por fecha, categoría y proveedor."""
    form = FiltroReporteForm(request.GET or None)
    ventas = Venta.objects.select_related('producto', 'producto__categoria', 'usuario').all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        categoria = form.cleaned_data.get('categoria')
        if fecha_inicio:
            ventas = ventas.filter(fecha__date__gte=fecha_inicio)
        if fecha_fin:
            ventas = ventas.filter(fecha__date__lte=fecha_fin)
        if categoria:
            ventas = ventas.filter(producto__categoria=categoria)

    total = ventas.aggregate(total=Sum(F('cantidad') * F('precio_unitario')))['total'] or 0

    return render(request, 'reportes/ventas.html', {
        'form': form,
        'ventas': ventas,
        'total': total,
    })


@login_required(login_url='login')
@solo_admin
def exportar_inventario_excel(request):
    """Exporta el inventario actual a Excel (.xlsx)."""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        messages.error(request, 'openpyxl no está instalado. Ejecuta: pip install openpyxl')
        return redirect('reporte_inventario')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Inventario'

    # Encabezados
    headers = ['ID', 'Nombre', 'Categoría', 'Proveedor', 'Precio', 'Stock', 'Stock Mínimo', 'Estado']
    header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    # Datos
    productos = Producto.objects.select_related('categoria', 'proveedor').all()
    for row, producto in enumerate(productos, 2):
        estado = 'BAJO STOCK' if producto.bajo_stock else 'OK'
        ws.append([
            producto.id,
            producto.nombre,
            producto.categoria.nombre,
            producto.proveedor.nombre,
            float(producto.precio),
            producto.stock,
            producto.stock_minimo,
            estado,
        ])
        if producto.bajo_stock:
            for col in range(1, 9):
                ws.cell(row=row, column=col).fill = PatternFill(
                    start_color='FFE0E0', end_color='FFE0E0', fill_type='solid'
                )

    # Ajustar anchos
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="inventario.xlsx"'
    return response


@login_required(login_url='login')
@solo_admin
def exportar_ventas_excel(request):
    """Exporta el reporte de ventas a Excel con los mismos filtros del reporte."""
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment
    except ImportError:
        messages.error(request, 'openpyxl no está instalado. Ejecuta: pip install openpyxl')
        return redirect('reporte_ventas')

    form = FiltroReporteForm(request.GET or None)
    ventas = Venta.objects.select_related('producto', 'producto__categoria', 'usuario').all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get('fecha_inicio')
        fecha_fin = form.cleaned_data.get('fecha_fin')
        categoria = form.cleaned_data.get('categoria')
        if fecha_inicio:
            ventas = ventas.filter(fecha__date__gte=fecha_inicio)
        if fecha_fin:
            ventas = ventas.filter(fecha__date__lte=fecha_fin)
        if categoria:
            ventas = ventas.filter(producto__categoria=categoria)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Ventas'

    headers = ['ID', 'Producto', 'Categoría', 'Cantidad', 'Precio Unitario', 'Total', 'Fecha', 'Usuario']
    header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')

    for venta in ventas:
        ws.append([
            venta.id,
            venta.producto.nombre,
            venta.producto.categoria.nombre,
            venta.cantidad,
            float(venta.precio_unitario),
            float(venta.total),
            venta.fecha.strftime('%Y-%m-%d %H:%M'),
            venta.usuario.username if venta.usuario else '-',
        ])

    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[col[0].column_letter].width = max_len + 4

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)

    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="ventas.xlsx"'
    return response
