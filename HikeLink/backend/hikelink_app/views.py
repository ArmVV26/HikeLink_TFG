import logging, shutil, os
from .models import User, Route, RouteRating, RouteComments, ForoThread, ForoComment, Favorites
from .serializers import (
    UserSerializer, RouteSerializer, RouteRatingSerializer,
    RouteCommentsSerializer, ForoThreadSerializer,
    ForoCommentSerializer, FavoriteSerializer,
    RegisterSerializer, UploadRouteSerializer,
    UpdateRouteSerializer, UpdateUserSerializer
)
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.conf import settings

"""Todas las clases heredan de ModelViewSet lo que proporciona automaticamente las operaciones de:
    - GET
    - POST
    - PUT
    - DELETE
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

class ForoThreadViewSet(viewsets.ModelViewSet):
    queryset = ForoThread.objects.all()
    serializer_class = ForoThreadSerializer

class ForoCommentViewSet(viewsets.ModelViewSet):
    queryset = ForoComment.objects.all()
    serializer_class = ForoCommentSerializer

class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        queryset = Favorites.objects.all()
        user = self.request.query_params.get('user')
        route = self.request.query_params.get('route')
        if user is not None:
            queryset = queryset.filter(user__id=user)
        if route is not None:
            queryset = queryset.filter(route__id=route)
        return queryset

# Vista para obtener los datos para el Token de Login
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response({
        'username': user.username,
        'profile_picture': user.profile_picture, 
        'full_name': user.full_name,
        'bio': user.bio,
        'id': user.id,
        'created_date': user.created_date,
        'email': user.email
    })

# Vista para obtener el rating del Usuario Logeado
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_rating(request, route_id):
    try:
        rating = RouteRating.objects.get(user=request.user, route_id=route_id)
        serializer = RouteRatingSerializer(rating)
        return Response(serializer.data)
    except RouteRating.DoesNotExist:
        return Response({"detail": "No rating found."}, status=404)
    
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

# Vista para hacer el registro del usuario
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

# Vista para actuliazar los datos del usuario
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)

    # Comprueba si el usuario es admin o el mismo usuario
    if request.user != user_to_edit and not request.user.is_staff:
        return Response({'detail': 'No tienes permiso para editar este perfil.'}, status=status.HTTP_403_FORBIDDEN)
    
    logout_required = False
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if old_password and new_password:
        if not user_to_edit.check_password(old_password):
            return Response({'detail': 'La contraseña actual es incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_to_edit.set_password(new_password)
        user_to_edit.save()
        logout_required = True

        if request.user == user_to_edit:
            for token in OutstandingToken.objects.filter(user=user_to_edit):
                try:
                    BlacklistedToken.objects.get_or_create(token=token)
                except Exception:
                    pass

    serializer = UpdateUserSerializer(instance=user_to_edit, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'message': 'Perfil actualizado correctamente', 'logout': logout_required}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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

# Vista para eliminar una Cuenta
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    if request.user != user_to_delete and not request.user.is_staff:
        return Response({'error': 'No tienes permiso para eliminar esta cuenta.'}, status=status.HTTP_403_FORBIDDEN)

    # Eliminar carpeta de usuario
    user_folder = os.path.join(settings.MEDIA_ROOT, user_to_delete.username)
    if os.path.exists(user_folder):
        shutil.rmtree(user_folder)

    # Eliminar comentarios, ratings y favoritos que haya hecho en otras rutas
    RouteComments.objects.filter(user=user_to_delete).delete()
    RouteRating.objects.filter(user=user_to_delete).delete()
    Favorites.objects.filter(user=user_to_delete).delete()
    ForoThread.objects.filter(user=user_to_delete).delete()
    ForoComment.objects.filter(user=user_to_delete).delete()

    for token in OutstandingToken.objects.filter(user=user_to_delete):
        try:
            BlacklistedToken.objects.get_or_create(token=token)
        except Exception:
            pass

    # Eliminar usuario (esto elimina tambien sus rutas por on_delete=CASCADE)
    user_to_delete.delete()

    return Response({'message': 'Cuenta eliminada correctamente.'}, status=status.HTTP_204_NO_CONTENT)