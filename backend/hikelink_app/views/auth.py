import logging, environ
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str

from ..serializers.auth import RegisterSerializer, ResetPasswordSerializer
from ..utils.email import send_password_reset_email
from ..models import User

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

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    env = environ.Env()

    email = request.data.get('email')
    if not email:
        return Response({"error": "Se requiere un correo electrónico."}, status=400)

    try:
        user = User.objects.get(email=email)
        url = env('URL_MAIN')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{url}/reset-password/{uid}/{token}/"
    
        send_password_reset_email(user.email, user.full_name, reset_link)
    except User.DoesNotExist:
        pass  

    return Response({"message": "Si el correo está registrado, se ha enviado un enlace para restablecer la contraseña."})

@api_view(['GET'])
@permission_classes([AllowAny])
def validate_reset_token(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            return Response({"valid": True, "username": user.username})
    except (User.DoesNotExist, ValueError):
        pass
    return Response({"valid": False}, status=400)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Contraseña restablecida correctamente"})
    return Response(serializer.errors, status=400)