from rest_framework import serializers
from ..models import Aula, Atividade
from .atividade_serializer import AtividadeSerializer

class AulaSerializer(serializers.ModelSerializer):
    atividades = AtividadeSerializer(many = True, read_only = True)
    atividades_ids = serializers.PrimaryKeyRelatedField(
        queryset=Atividade.objects.all(),
        source='atividades',
        write_only=True,
        many=True,
        allow_empty=True,
        required=False
    )
    class Meta:
        model = Aula
        fields = [
            'id',
            'titulo',
            'descricao',
            'conteudo',
            'atividades_ids',
            'atividades',
        ]
        read_only_fields = ('id',)
        extra_kwargs = {
            'titulo': {'required': True, 'allow_blank': False},
            'descricao': {'required': True, 'allow_blank': False},
            'conteudo': {'required': False, 'allow_blank': True},
        }    
