import uuid, markdown, os, logging
from rest_framework import serializers
from .models import User, Route, RouteRating, RouteComments, ForoThread, ForoComment, Favorites
from django.db.models import Avg
from django.utils.safestring import mark_safe
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.utils.text import slugify

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'profile_picture']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RouteRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteRating
        fields = '__all__'

class RouteCommentsSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True) 

    class Meta:
        model = RouteComments
        fields = '__all__'
        read_only_fields = ['user']

class RouteSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True) 
    comments = RouteCommentsSerializer(source='routecomments_set', many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    description_html = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = '__all__'

    def get_average_rating(self, obj):
        return obj.routerating_set.aggregate(avg=Avg('rating'))['avg']
    
    def get_description_html(self, obj):
        return mark_safe(markdown.markdown(obj.description))

class ForoCommentSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = ForoComment
        fields = '__all__'

class ForoThreadSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    comments = ForoCommentSerializer(source='forocomment_set', many=True, read_only=True)

    class Meta:
        model = ForoThread
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

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

    # Metodo que crea la carpeta y guarda la imagen que ha subido el usuario
    def create(self, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        username = validated_data['username']

        # Crea el usuario sin imagen aún
        user = User.objects.create_user(**validated_data)

        # Crear carpeta personalizada por usuario
        user_folder = os.path.join(settings.MEDIA_ROOT, username)
        os.makedirs(user_folder, exist_ok=True)


        if profile_picture:
            # Crear un nombre único, limpio y rastreable
            ext = profile_picture.name.split('.')[-1]
            filename = f"{slugify(username)}-{uuid.uuid4().hex[:8]}.{ext}"
            
            # Guarda la imagen en la carpeta del usuario
            file_path = os.path.join(user_folder, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in profile_picture.chunks():
                    destination.write(chunk)
            # Guarda solo el nombre de la imagen
            user.profile_picture = filename
            user.save()
            
        return user
    
class UploadRouteSerializer(serializers.ModelSerializer):
    """Clase usada en el registro de una ruta que se encarga de hacer:
        - Recoger y serializar todas las imagenes.
        - Generar el slug del titulo.
        - Crear una carpeta con ese slug.
        - Guardar el archivo GPX renombrado con el slug.
        - Guardar todas las imagenes con el nombre adecuado.
        - Devolver todos los datos de la ruta.
    """
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    gpxFile = serializers.FileField(write_only=True)

    class Meta:
        model = Route
        fields = ['title', 'type', 'description', 'difficulty', 'origin', 'images',
                  'gpxFile', 'start_latitude', 'start_longitude', 'duration', 'distance']
        
    # Metodo que crea dentro de la carpeta del usuario, una carpeta con el slug
    # de la ruta y dentro las imagenes y el archivo gpx con el slug.
    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        # Obtengo el titulo, lo valido y convierto a slug
        title = validated_data['title']
        slug = slugify(title)

        # Busco la carpeta del usuario y creo la carpeta con el slug
        user_folder = os.path.join(settings.MEDIA_ROOT, user.username)
        route_folder = os.path.join(user_folder, slug)
        os.makedirs(route_folder, exist_ok=True)

        # Guardo el archivo GPX dentro de la carpeta anterior 
        gpx_file = validated_data.pop('gpxFile')
        gpx_filename = f"{slug}.gpx"
        gpx_path = os.path.join(route_folder, gpx_filename)
        with open(gpx_path, 'wb+') as f:
            for chunk in gpx_file.chunks():
                f.write(chunk)

        # Guardar imaganes de la ruta
        images = validated_data.pop('images', [])
        img_filenames = []
        for i, image in enumerate(images):
            ext = image.name.split('.')[-1]
            filename = f"{i+1}_img.{ext}"
            path = os.path.join(route_folder, filename)
            with open(path, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            img_filenames.append(filename)
        
        route = Route.objects.create(
            user=user,
            slug=slug,
            gpx_file=gpx_filename,
            img=img_filenames,
            start_latitude=validated_data.get('start_latitude'),
            start_longitude=validated_data.get('start_longitude'),
            duration=validated_data.get('duration'),
            distance=validated_data.get('distance'),
            **{k: v for k, v in validated_data.items() if k in ['title', 'type', 'description', 'difficulty', 'origin']}
        )
        return route
    
class UpdateRouteSerializer(serializers.ModelSerializer):
    """Clase que se encarga de actualizar los datos de la ruta:
        - Recoge todos los datos.
        - Borrar imagenes si se sube imagenes.
        - Guardar las imagenes con el nombre adecuado.
        - Actualizar todos los campos.
    """
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Route
        fields = ['title', 'type', 'description', 'difficulty', 'origin', 'images']

    def update(self, instance, validated_data):
        request = self.context['request']
        user = request.user

        title = validated_data.get('title', instance.title)
        slug = instance.slug

        user_folder = os.path.join(settings.MEDIA_ROOT, user.username)
        route_folder = os.path.join(user_folder, slug)

        # Eliminar imágenes antiguas si se suben nuevas
        new_images = validated_data.pop('images', None)
        if new_images is not None:
            for filename in os.listdir(route_folder):
                if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    os.remove(os.path.join(route_folder, filename))

            # Guardar nuevas imágenes
            img_filenames = []
            for i, image in enumerate(new_images):
                ext = image.name.split('.')[-1]
                filename = f"{i+1}_img.{ext}"
                path = os.path.join(route_folder, filename)
                with open(path, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)
                img_filenames.append(filename)
            instance.img = img_filenames

        # Actualizar otros campos
        instance.title = title
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.origin = validated_data.get('origin', instance.origin)

        instance.save()
        return instance
    
class UpdateUserSerializer(serializers.ModelSerializer):
    """Clase que se encarga de actualizar un usuario:
        - Busca si hay una nueva imagen de perfil.
        - Si hay borra la que hay y añade la nueva.
    """
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['full_name', 'bio', 'email', 'profile_picture']

    def update(self, instance, validated_data):
        # Actualizar campos simples
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.email = validated_data.get('email', instance.email)

        # Imagen
        new_image = validated_data.get('profile_picture')
        if new_image:
            # Eliminar imagen anterior si existe
            if instance.profile_picture:
                old_path = os.path.join(settings.MEDIA_ROOT, instance.username, str(instance.profile_picture))
                if os.path.exists(old_path):
                    os.remove(old_path)

            # Guardar nueva imagen con nombre personalizado
            user_folder = os.path.join(settings.MEDIA_ROOT, instance.username)
            ext = new_image.name.split('.')[-1]
            filename = f"{slugify(instance.username)}-{uuid.uuid4().hex[:8]}.{ext}"
            file_path = os.path.join(user_folder, filename)

            with open(file_path, 'wb+') as destination:
                for chunk in new_image.chunks():
                    destination.write(chunk)

            instance.profile_picture = filename

        instance.save()
        return instance