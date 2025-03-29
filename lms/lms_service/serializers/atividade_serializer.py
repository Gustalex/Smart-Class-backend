from rest_framework import serializers
from ..models import Atividade

class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {
            'titulo': {'required': True, 'allow_blank': False},
            'descricao': {'required': True, 'allow_blank': False},
            'data_entrega': {'required': True},
        }