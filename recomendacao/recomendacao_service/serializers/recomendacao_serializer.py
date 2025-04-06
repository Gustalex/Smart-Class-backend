from rest_framework import serializers
from ..models import Recomendacao


class RecomendacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacao
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'aluno': {'required': True},
            'atividade': {'required': True},
            'feedback': {'required': True},
        }
