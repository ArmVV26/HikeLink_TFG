from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination

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
