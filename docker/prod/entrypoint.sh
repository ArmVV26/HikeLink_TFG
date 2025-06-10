#!/bin/sh

echo "🧹 Limpiando la base de datos..."
python manage.py flush --noinput

echo "▶️ Ejecutando migraciones..."
python manage.py migrate --noinput

echo "👤 Creando superusuario..."
python create_superuser.py

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "🔧 Configurando archivos estáticos del admin..."
python manage.py collectstatic --noinput --clear --no-post-process

echo "💼 Cargando los datos base..."
python manage.py shell < hikelink_app/populate.py

echo "🚀 Lanzando aplicación..."
exec "$@"
