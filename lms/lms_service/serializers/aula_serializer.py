import os
from rest_framework import serializers
from ..models import Aula
from .atividade_serializer import AtividadeSerializer


class AulaSerializer(serializers.ModelSerializer):
    atividades = AtividadeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Aula
        fields = '__all__'
        read_only_fields = ('id',)

    
    def validate_conteudo(self, arquivo):
        if arquivo:
            max_size = 50 * 1024 * 1024
            if arquivo.size > max_size:
                raise serializers.ValidationError("O arquivo é muito grande. Tamanho máximo permitido é 50MB.")
            
            valid_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.txt', 
                               '.zip', '.rar', '.mp4', '.mov', '.avi', '.jpg', '.png']
            ext = os.path.splitext(arquivo.name)[1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    f"Tipo de arquivo não suportado. Extensões permitidas: {', '.join(valid_extensions)}"
                )
            
            if len(arquivo.name) > 100:
                raise serializers.ValidationError("Nome do arquivo muito longo. Máximo de 100 caracteres.")
            
            if arquivo.size == 0:
                raise serializers.ValidationError("O arquivo está vazio.")
            
            forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
            if any(char in arquivo.name for char in forbidden_chars):
                raise serializers.ValidationError("Nome do arquivo contém caracteres inválidos.")
        
        return arquivo