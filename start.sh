#!/usr/bin/env bash
# start.sh — Script de inicio para Render
# Este script se ejecuta ANTES de iniciar gunicorn

echo "=== INICIANDO SERVIDOR ==="

echo "🗄️ Ejecutando migraciones..."
python manage.py migrate --no-input

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "👤 Configurando datos iniciales..."
python setup_production.py

echo "🚀 Iniciando Gunicorn..."
exec gunicorn inventario.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
