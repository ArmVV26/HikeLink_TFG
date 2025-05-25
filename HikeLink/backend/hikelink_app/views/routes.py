import logging, shutil, os
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from django.conf import settings

from ..models import User, Route, RouteComments, RouteRating, Favorites
from ..serializers.routes import RouteSerializer, RouteCommentsSerializer, RouteRatingSerializer, UpdateRouteSerializer, UploadRouteSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RouteRatingViewSet(viewsets.ModelViewSet):
    queryset = RouteRating.objects.all()
    serializer_class = RouteRatingSerializer

class RouteCommentsViewSet(viewsets.ModelViewSet):
    queryset = RouteComments.objects.all()
    serializer_class = RouteCommentsSerializer

    # Metodo que asigna automaticamente el usuario autenticado al crear un comentario
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Vista para obtener el rating del Usuario Logeado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rating(request, route_id):
    try:
        rating = RouteRating.objects.get(user=request.user, route_id=route_id)
        serializer = RouteRatingSerializer(rating)
        return Response(serializer.data)
    except RouteRating.DoesNotExist:
        return Response({"detail": "No rating found."}, status=status.HTTP_404_NOT_FOUND)
    
# Clase para establecer la paginacion predeterminada
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

# Vista para obtener las rutas de un usuario
@api_view(['GET'])
@permission_classes([AllowAny])
# Si solamente se quiere para el usuario autenticado
# @permission_classes([IsAuthenticated])
def get_routes_by_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    routes = Route.objects.filter(user=user).order_by('created_date')
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(routes, request)
    serializer = RouteSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# Vista para obtener todas las rutas paginadas
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_routes(request):
    routes = Route.objects.all().order_by('-created_date')
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(routes, request)
    serializer = RouteSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# Vista para filtrar las rutas por parametros
@api_view(['GET'])
@permission_classes([AllowAny])
def filter_routes(request):
    routes = Route.objects.all()

    title = request.GET.get('title')
    type_ = request.GET.get('type')
    difficulty = request.GET.get('difficulty')
    origin = request.GET.get('origin')
    duration_min = request.GET.get('duration_min')
    duration_max = request.GET.get('duration_max')
    distance_min = request.GET.get('distance_min')
    distance_max = request.GET.get('distance_max')

    if title:
        routes = routes.filter(title__icontains=title)  # 🔍 búsqueda parcial

    if type_ and type_ != 'Todas':
        routes = routes.filter(type=type_)

    if difficulty and difficulty != 'Todas':
        routes = routes.filter(difficulty=difficulty)

    if origin and origin != 'Todos':
        routes = routes.filter(origin=origin)

    if duration_min and duration_max and not (duration_min == '0' and duration_max == '24'):
        routes = routes.filter(duration__gte=duration_min, duration__lte=duration_max)

    if distance_min and distance_max and not (distance_min == '0' and distance_max == '1000'):
        routes = routes.filter(distance__gte=distance_min, distance__lte=distance_max)
        
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(routes.order_by('-created_date'), request)
    serializer = RouteSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# Vista para hacer el registro de una ruta
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_route(request):
    serializer = UploadRouteSerializer(data=request.data, context={'request': request})
    try:
        if serializer.is_valid():
            route = serializer.save()
            return Response({'id': route.id, 'slug': route.slug, "message": "Ruta subida correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except IntegrityError as e:
        if 'slug' in str(e):
            return Response({'error': 'Ya existe una ruta con este título.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Error al guardar la ruta.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Vista para actualizar la ruta
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_route(request, route_id):
    try:
        route = Route.objects.get(id=route_id, user=request.user)
    except Route.DoesNotExist:
        return Response({'error': 'Ruta no encontrada o no autorizada'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateRouteSerializer(route, data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Ruta actualizada correctamente"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para eliminar una Ruta
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_route(request, route_id):
    try:
        route = Route.objects.get(id=route_id)
    except Route.DoesNotExist:
        return Response({'error': 'Ruta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.user != route.user and not request.user.is_staff:
        return Response({'error': 'No tienes permiso para eliminar esta ruta.'}, status=status.HTTP_403_FORBIDDEN)

    # Eliminar comentarios, puntuaciones, favoritos (si no tienes on_delete=CASCADE)
    RouteComments.objects.filter(route=route).delete()
    RouteRating.objects.filter(route=route).delete()
    Favorites.objects.filter(route=route).delete()

    # Eliminar carpeta con imágenes y GPX
    user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
    route_folder = os.path.join(user_folder, route.slug)
    if os.path.exists(route_folder):
        shutil.rmtree(route_folder)

    route.delete()
    return Response({'message': 'Ruta eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)