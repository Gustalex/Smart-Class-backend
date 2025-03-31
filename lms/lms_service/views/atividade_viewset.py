from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Atividade
from ..serializers import AtividadeSerializer
import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404


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
    

