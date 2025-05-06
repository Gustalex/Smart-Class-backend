from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Atividade, Turma, Aula
from ..serializers import AtividadeSerializer
import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.db import models


class AtividadeViewSet(viewsets.ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer

    @action(detail=True, methods=['get'])
    def download_conteudo(self, request, pk=None):
        atividade = get_object_or_404(Atividade, pk=pk)

        file_path = atividade.conteudo.path
        if not os.path.exists(file_path):
            return Response({'error': 'Arquivo não encontrado no servidor'}, status=status.HTTP_404_NOT_FOUND)
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream' 
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    

    @action(detail=True, methods=['get'])
    def get_atividades_usuario(self, request, pk=None):
        try:
            user_id = int(pk) 
            if not user_id:
                return Response(
                    {"error": "ID de usuário inválido"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            all_turmas = Turma.objects.all()
            turmas_aluno = [t for t in all_turmas if user_id in t.alunos]
            
            if not turmas_aluno:
                turmas_professor = Turma.objects.filter(professor=user_id)
                aulas = Aula.objects.filter(turma__in=turmas_professor)
            else:
                aulas = Aula.objects.filter(turma__in=turmas_aluno)
            
            atividades_ids = list(aulas.exclude(atividade__isnull=True).values_list('atividade', flat=True))
            atividades = Atividade.objects.filter(
                models.Q(aula__in=aulas) | 
                models.Q(id__in=atividades_ids)
            ).distinct()

            if atividades.exists():
                serializer = AtividadeSerializer(atividades, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {"error": "Usuário não possui atividades cadastradas"},
                status=status.HTTP_404_NOT_FOUND
            )

        except ValueError:
            return Response(
                {"error": "ID de usuário deve ser um número"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
