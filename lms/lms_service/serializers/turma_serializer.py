from rest_framework import serializers
from ..models import Turma, Curso
from .curso_serializer import CursoSerializer

class TurmaSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(),
        source='curso',
        write_only=True,
        required=True
    )

    class Meta:
        model = Turma
        fields = [
            'id', 'nome', 'curso_id', 'curso', 
            'materia', 'professor', 'alunos'
        ]
        read_only_fields = ('id',)
        extra_kwargs = {
            'nome': {'required': True, 'allow_blank': False},
            'materia': {'required': True, 'allow_blank': False},
            'professor': {'required': True},
            'alunos': {'required': False, 'allow_null': True},
        }

    def validate_alunos(self, value):
        if value is None:
            return []
        if not isinstance(value, (list, dict)):
            raise serializers.ValidationError("Alunos deve ser uma lista ou objeto JSON.")
        return value

    def create(self, validated_data):
        validated_data.setdefault('alunos', [])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance