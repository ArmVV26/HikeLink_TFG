import uuid, os, logging
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.password_validation import validate_password
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

from ..models import User, Favorites

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

class UpdateUserSerializer(serializers.ModelSerializer):
    """Clase que se encarga de actualizar un usuario:
        - Busca si hay una nueva imagen de perfil.
        - Si hay borra la que hay y añade la nueva.
    """
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    old_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['full_name', 'bio', 'email', 'profile_picture', 'old_password', 'new_password']
    
    # VALIDACIONES 
    def validate_email(self, value):
        try:
            django_validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Correo electrónico inválido.")
        return value

    def validate_full_name(self, value):
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError("El nombre no puede contener números.")
        return value

    def validate(self, data):
        new_password = data.get('new_password')
        if new_password:
            validate_password(new_password, user=self.instance)
        return data

    def update(self, instance, validated_data):
        self.logout_required = False

        # Cambio de contraseña
        old_password = validated_data.pop('old_password', None)
        new_password = validated_data.pop('new_password', None)

        if old_password and new_password:
            if not instance.check_password(old_password):
                raise ValidationError({'detail': 'La contraseña actual es incorrecta.'})
            instance.set_password(new_password)
            self.logout_required = True

            # Logout para todos los tokens (si se desea invalidar tokens activos)
            for token in OutstandingToken.objects.filter(user=instance):
                try:
                    BlacklistedToken.objects.get_or_create(token=token)
                except Exception:
                    pass

        # Actualizar campos simples
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)

        # Imagen
        new_image = validated_data.get('profile_picture')
        if new_image:
            # Eliminar imagen anterior si existe
            if instance.profile_picture:
                try:
                    old_path = default_storage.path(instance.profile_picture.name)
                    default_storage.delete(old_path)
                except Exception:
                    pass 

            # Guardar nueva imagen con nombre personalizado
            ext = new_image.name.split('.')[-1]
            filename = f"{slugify(instance.username)}-{uuid.uuid4().hex[:8]}.{ext}"
            file_path = f"{instance.username}/{filename}"
            default_storage.save(file_path, ContentFile(new_image.read()))
            instance.profile_picture = filename

        instance.save()
        return instance