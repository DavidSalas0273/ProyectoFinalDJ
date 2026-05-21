#!/usr/bin/env bash
# build.sh — Script de build para Render
set -o errexit   # salir si cualquier comando falla

echo "🔧 Instalando dependencias..."
pip install -r requirements.txt

echo "🗄️ Ejecutando migraciones..."
python manage.py makemigrations --check || python manage.py makemigrations
python manage.py migrate

echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --no-input

echo "👤 Creando superusuario..."
python create_superuser.py

echo "📦 Cargando datos iniciales..."
python load_initial_data.py

echo "✅ Build completado exitosamente"
