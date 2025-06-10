import os
import django
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def create_superuser():
    User = get_user_model()
    
    # Obtener credenciales del entorno
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    
    # Verificar que todas las credenciales esten presentes
    if not all([username, email, password]):
        print("Error: Faltan credenciales del superusuario en las variables de entorno")
        return
    
    try:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=username).exists():
            print(f"El superusuario '{username}' ya existe")
            return
        
        # Crear el superusuario
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Superusuario '{username}' creado exitosamente")
        
    except ValidationError as e:
        print(f"Error de validación: {e}")
    except Exception as e:
        print(f"Error al crear el superusuario: {e}")

if __name__ == '__main__':
    create_superuser() 