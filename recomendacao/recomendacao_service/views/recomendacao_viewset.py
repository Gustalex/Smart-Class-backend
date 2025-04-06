from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..serializers import RecomendacaoSerializer
from ..models import Recomendacao

class RecomendacaoViewSet(ModelViewSet):
    queryset = Recomendacao.objects.all()
    serializer_class = RecomendacaoSerializer

    @action(detail=True, methods=['get'])
    def get_aluno_recomendacoes(self, request, pk=None):
        aluno_id = pk
        recomendacoes = Recomendacao.objects.filter(aluno=aluno_id)
        if not recomendacoes.exists():
            return Response(
                {'detail': 'Nenhuma recomendação encontrada para este aluno'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(recomendacoes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'])
    def delete_atividade_recomendacao(self, request, pk=None):
        atividade_id = pk
        recomendacoes = Recomendacao.objects.filter(atividade=atividade_id)

        if not recomendacoes.exists():
            return Response(
                {'detail': 'Nenhuma recomendação encontrada para esta atividade'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        recomendacoes.delete()
        return Response(
            {'detail': 'Recomendações deletadas com sucesso'}, 
            status=status.HTTP_204_NO_CONTENT
        )
    
        
