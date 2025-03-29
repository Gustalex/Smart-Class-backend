from rest_framework import serializers
from ..models import Curso

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'nome': {'required': True, 'allow_blank': False}
        }
    

