import markdown, os, logging
from rest_framework import serializers
from django.db.models import Avg
from django.utils.safestring import mark_safe
from django.conf import settings
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from ..models import Route, RouteRating, RouteComments
from ..serializers.users import PublicUserSerializer

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

        # Asigno el nombre de la carpeta
        route_folder = f"{user.username}/{slug}/"

        # Guardo el archivo GPX dentro de la carpeta anterior 
        gpx_file = validated_data.pop('gpxFile')
        gpx_filename = f"{slug}.gpx"
        gpx_path = f"{route_folder}{gpx_filename}"
        default_storage.save(gpx_path, ContentFile(gpx_file.read()))

        # Guardar imaganes de la ruta
        images = validated_data.pop('images', [])
        img_filenames = []
        for i, image in enumerate(images):
            ext = image.name.split('.')[-1]
            filename = f"{i+1}_img.{ext}"
            path = f"{route_folder}{filename}"
            default_storage.save(path, ContentFile(image.read()))
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
        slug = instance.slug

        route_folder = f"{user.username}/{slug}/"

        # Eliminar imágenes antiguas si se suben nuevas
        new_images = validated_data.pop('images', None)
        if new_images is not None:
            _, existing_files = default_storage.listdir(route_folder)
            for filename in existing_files:
                if filename.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    default_storage.delete(f"{route_folder}{filename}")

            # Guardar nuevas imágenes
            img_filenames = []
            for i, image in enumerate(new_images):
                ext = image.name.split('.')[-1]
                filename = f"{i+1}_img.{ext}"
                path = f"{route_folder}{filename}"
                default_storage.save(path, ContentFile(image.read()))
                img_filenames.append(filename)
            instance.img = img_filenames

        # Actualizar otros campos
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.origin = validated_data.get('origin', instance.origin)

        instance.save()
        return instance