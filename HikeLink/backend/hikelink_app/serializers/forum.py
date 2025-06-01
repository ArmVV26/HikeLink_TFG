import re
from rest_framework import serializers
from ..models import User, ForoThread, ForoComment
from ..serializers.users import PublicUserSerializer

class ForoCommentSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = ForoComment
        fields = '__all__'

class ForoThreadSerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    comments = ForoCommentSerializer(source='forocomment_set', many=True, read_only=True)
    comments_count = serializers.IntegerField(source='forocomment_set.count', read_only=True)

    class Meta:
        model = ForoThread
        fields = '__all__'

    # Validacion
    def validate_title(self, value):
        title_regex = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s\-.,!?¿¡]+$"
        if not re.fullmatch(title_regex, value):
            raise serializers.ValidationError("El título contiene caracteres no permitidos.")
        return value