from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'cpf', 'email', 'role', 'curso', 'cursos','turmas', 'password',
                 'is_student', 'is_teacher', 'is_manager', 'created_at', 'updated_at')
        extra_kwargs = {
            'cursos': {'required': False},
            'curso': {'required': False, 'allow_null': True},
            'turmas': {'required': False, 'allow_null': True},
        }

    def validate(self, data):
        role = data.get('role')
        curso = data.get('curso')
        cursos = data.get('cursos', [])

        if 'role' in data:
            if (role == 'student' or role is None) and not curso and not (self.instance and self.instance.curso):
                raise serializers.ValidationError(
                    {"curso": "O campo 'curso' é obrigatório para alunos."}
                )

            if role == 'teacher' and not cursos and not (self.instance and self.instance.cursos):
                raise serializers.ValidationError(
                    {"cursos": "O campo 'cursos' é obrigatório para professores."}
                )

            if role == 'student' and cursos:
                raise serializers.ValidationError(
                    {"cursos": "Alunos não podem estar associados a múltiplos cursos."}
                )

            if role == 'teacher' and curso:
                raise serializers.ValidationError(
                    {"curso": "Professores devem usar o campo 'cursos'."}
                )

        return data

    def validate_turmas(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError("O campo turmas deve ser uma lista.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', None)
        curso = validated_data.pop('curso', None)
        cursos = validated_data.pop('cursos', [])
        turmas = validated_data.pop('turmas', [])

        user = User.objects.create_user_entity(
            role=role,
            password=password,
            curso=curso,
            cursos=cursos,
            turmas=turmas,
            **validated_data
        )
        return user
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.cpf = validated_data.get('cpf', instance.cpf)

        role = validated_data.get('role')
        
        if role is not None:
            instance.is_student = False
            instance.is_teacher = False
            instance.is_manager = False

            if role == 'student':
                instance.is_student = True
                instance.curso = validated_data.get('curso', instance.curso)
                instance.cursos = []
                instance.turmas = validated_data.get('turmas', instance.turmas or [])
            elif role == 'teacher':
                instance.is_teacher = True
                instance.curso = None
                instance.cursos = validated_data.get('cursos', instance.cursos or [])
                instance.turmas = validated_data.get('turmas', instance.turmas or [])
            elif role == 'manager':
                instance.is_manager = True
                instance.curso = None
                instance.cursos = []
                

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance
    
class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(cpf=attrs['cpf'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('Incorrect credentials')
        return {'user': user}

    