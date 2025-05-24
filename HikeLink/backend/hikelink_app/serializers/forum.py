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

    class Meta:
        model = ForoThread
        fields = '__all__'