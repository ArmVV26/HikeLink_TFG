import logging, shutil, os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from ..serializers.auth import RegisterSerializer

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

# Vista para hacer el registro del usuario
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Usuario registrado correctamente"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)