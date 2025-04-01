from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ..serializers import TurmaSerializer
from ..models import Turma
from ..helpers import make_request_to_auth


class TurmaViewSet(ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer


    def perform_create(self, serializer):
        turma = serializer.save()

        request_data = {"turmas": [turma.id]}

        response = make_request_to_auth(
            request=self.request,
            method="patch",
            endpoint=f"api/auth/users/{turma.professor}/update/",
            data=request_data
        )

        if response and response.status_code == 200:
            return Response(
                {
                    "message": "Turma criada e professor atualizado com sucesso",
                    "turma": TurmaSerializer(turma).data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            turma.delete()
            return Response(
                {
                    "error": "Falha ao atualizar professor",
                    "turma": TurmaSerializer(turma).data
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
    
    @action(detail=True, methods=['patch'])
    def update_alunos_turma(self, request, pk=None):
        with transaction.atomic():
            turma = self.get_object()
            alunos = request.data.get('alunos', [])
            
            if not isinstance(alunos, list):
                return Response(
                    {"error": "O campo alunos deve ser uma lista"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            turma.alunos = list(set(alunos))
            turma.save()
            
            request_data = {"turmas": [turma.id]}
            success_count = 0
            
            for aluno_id in alunos:
                response = make_request_to_auth(
                    request=request,
                    method="patch",
                    endpoint=f"api/auth/users/{aluno_id}/update/",
                    data=request_data
                )
                
                if response and response.status_code == 200:
                    success_count += 1
            
            if success_count == len(alunos):
                return Response(
                    {
                        "message": "Turma e alunos atualizados com sucesso",
                        "turma": TurmaSerializer(turma).data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                turma.refresh_from_db()
                return Response(
                    {
                        "error": f"Atualizou {success_count} de {len(alunos)} alunos",
                        "turma": TurmaSerializer(turma).data
                    },
                    status=status.HTTP_207_MULTI_STATUS
                )