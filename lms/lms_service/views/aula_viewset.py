from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Aula, Turma
from ..serializers import AulaSerializer
import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404

class AulaViewSet(viewsets.ModelViewSet):
    queryset = Aula.objects.all()
    serializer_class = AulaSerializer

    @action(detail=True, methods=['get'])
    def download_conteudo(self, request, pk=None):
        aula = get_object_or_404(Aula, pk=pk)
        
        file_path = aula.conteudo.path
        if not os.path.exists(file_path):
            return Response({'detail': 'Arquivo não encontrado no servidor'}, status=status.HTTP_404_NOT_FOUND)
        
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream' 
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response
    
    @action(detail=True, methods=['get'])
    def get_aulas_turma(self, request, pk=None):
        try:
            turma = get_object_or_404(Turma, pk=pk)
            aulas = turma.aulas.all()
            serializer = self.get_serializer(aulas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Turma.DoesNotExist:
            return Response({'detail': 'Turma não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
