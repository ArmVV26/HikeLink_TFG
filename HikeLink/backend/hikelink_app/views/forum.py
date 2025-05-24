from rest_framework import viewsets

from ..models import ForoThread, ForoComment
from ..serializers.forum import ForoThreadSerializer, ForoCommentSerializer

class ForoThreadViewSet(viewsets.ModelViewSet):
    queryset = ForoThread.objects.all()
    serializer_class = ForoThreadSerializer

class ForoCommentViewSet(viewsets.ModelViewSet):
    queryset = ForoComment.objects.all()
    serializer_class = ForoCommentSerializer