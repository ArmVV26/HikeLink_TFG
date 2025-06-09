#!/bin/sh

echo "▶️ Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "🚀 Lanzando aplicación..."
exec "$@"
