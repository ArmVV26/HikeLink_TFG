from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from ..models import ForoThread, ForoComment
from ..serializers.forum import ForoThreadSerializer, ForoCommentSerializer

class ForoThreadViewSet(viewsets.ModelViewSet):
    queryset = ForoThread.objects.all()
    serializer_class = ForoThreadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ForoCommentViewSet(viewsets.ModelViewSet):
    queryset = ForoComment.objects.all()
    serializer_class = ForoCommentSerializer

    # Metodo que asigna automaticamente el usuario autenticado al crear un comentario
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Clase para establecer la paginacion predeterminada
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50

# Vista para obtener todos los hilos del foro
@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_threads(request):
    thread = ForoThread.objects.all().order_by('-created_date')
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(thread, request)
    serializer = ForoThreadSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)


# Vista para filtrar los hilos por titulo
@api_view(['GET'])
@permission_classes([AllowAny])
def filter_threads(request):
    thread = ForoThread.objects.all()

    title = request.GET.get('title')

    if title:
        thread = thread.filter(title__icontains=title)  
        
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(thread.order_by('-created_date'), request)
    serializer = ForoThreadSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# Vista para eliminar un Hilo
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_thread(request, thread_id):
    try:
        thread = ForoThread.objects.get(id=thread_id)
    except ForoThread.DoesNotExist:
        return Response({'error': 'Hilo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Permitir solo al autor o admin
    if request.user != thread.user and not request.user.is_staff:
        return Response({'error': 'No tienes permiso para eliminar este hilo.'}, status=status.HTTP_403_FORBIDDEN)

    # Eliminar comentarios asociados
    ForoComment.objects.filter(thread=thread).delete()

    # Eliminar hilo
    thread.delete()
    return Response({'message': 'Hilo eliminado correctamente.'}, status=status.HTTP_204_NO_CONTENT)