import os
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import AvaliacaoAtividade
from ..serializers import AvaliacaoAtividadeSerializer

class AvaliacaoAtividadeViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoAtividade.objects.all()
    serializer_class = AvaliacaoAtividadeSerializer

    @action(detail=False, methods=['get'], url_path='aluno/(?P<id_aluno>\d+)/atividade/(?P<id_atividade>\d+)')
    def download_conteudo_avaliacao(self, request, id_aluno=None, id_atividade=None):
        try:
            avaliacao = get_object_or_404(
                AvaliacaoAtividade, 
                aluno=id_aluno, 
                atividade=id_atividade
            )
            
            if not avaliacao.conteudo_para_avaliacao:
                return Response(
                    {'detail': 'Nenhum arquivo foi enviado para esta atividade'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
            file_path = avaliacao.conteudo_para_avaliacao.path
            if not os.path.exists(file_path):
                return Response(
                    {'detail': 'Arquivo não encontrado no servidor'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
            
        except Exception as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    @action(detail=True, methods=['get'])
    def get_atividades_by_id(self, request, pk=None):
        try:
            atividades = AvaliacaoAtividade.objects.filter(atividade = pk)
            if not atividades.exists():
                return Response(
                    {'detail': 'Nenhuma atividade encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            serializer = self.get_serializer(atividades, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AvaliacaoAtividade.DoesNotExist:
            return Response(
                {'detail': 'Avaliação não encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )