import uuid, re, logging
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from ..utils.email import send_welcome_email

from ..models import User

class RegisterSerializer(serializers.ModelSerializer):
    """Clase usada en el registro del usuario que se encarga de hacer:
        - Validar el email y username para que sean unicos.
        - Verificar la contraseña.
        - Permite una imagen de perfil.
        - Crea una carpeta propia del usuario.
        - Usa un nombre limpio y único para la imagen.
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este correo ya está registrado.")]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este nombre de usuario ya está en uso.")]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'full_name', 'password', 'bio', 'profile_picture')

    # VALIDACIONES
    def validate_email(self, value):
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Correo electrónico no válido.")
        return value

    def validate_full_name(self, value):
        if not re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", value):
            raise serializers.ValidationError("El nombre no puede contener números ni caracteres especiales.")
        return value

    def validate_username(self, value):
        if ' ' in value:
            raise serializers.ValidationError("El nombre de usuario no puede contener espacios.")
        if not re.fullmatch(r"^[a-zA-Z0-9._-]{5,}$", value):
            raise serializers.ValidationError("El nombre de usuario debe tener al menos 5 caracteres y solo puede incluir letras, números, puntos, guiones y guiones bajos.")
        return value

    def validate_password(self, value):
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        if not re.fullmatch(pattern, value):
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un símbolo.")
        validate_password(value)  # Aplica validaciones de Django también
        return value

    # Metodo que crea la carpeta y guarda la imagen que ha subido el usuario
    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        username = validated_data['username']

        # Crea el usuario sin imagen aún
        user = User.objects.create_user(**validated_data)

        if profile_picture:
            # Crear nombre de archivo limpio y unico
            ext = profile_picture.name.split('.')[-1]
            filename = f"{slugify(username)}-{uuid.uuid4().hex[:8]}.{ext}"
            file_path = f"{username}/{filename}"

            # Guardar imagen en el storage
            default_storage.save(file_path, ContentFile(profile_picture.read()))

            # Asignar ruta al ImageField y guardar
            user.profile_picture = filename
            user.save()

            # Validación tras guardar
            if not default_storage.exists(user.profile_picture):
                raise Exception("Fallo al guardar la imagen de perfil")
        
        # Mandar el correo de bienvenida
        send_welcome_email(user.email, user.full_name)

        return user