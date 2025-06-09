#!/bin/sh

echo "▶️ Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "💼 Cargando los datos base..."
python manage.py shell < hikelink_app/populate.py

echo "🚀 Lanzando aplicación..."
exec "$@"
