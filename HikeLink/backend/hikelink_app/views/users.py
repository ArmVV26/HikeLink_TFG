import logging, shutil, os
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.conf import settings

from ..models import User, RouteRating, RouteComments, ForoThread, ForoComment, Favorites
from ..serializers.users import UserSerializer, UpdateUserSerializer, FavoriteSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

# Vista para actuliazar los datos del usuario
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_profile(request, user_id):
    user_to_edit = get_object_or_404(User, id=user_id)

    # Comprueba si el usuario es admin o el mismo usuario
    if request.user != user_to_edit and not request.user.is_staff:
        return Response({'detail': 'No tienes permiso para editar este perfil.'}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = UpdateUserSerializer(instance=user_to_edit, data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({'message': 'Perfil actualizado correctamente', 
                             'logout': getattr(serializer, 'logout_required', False)}, 
                             status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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