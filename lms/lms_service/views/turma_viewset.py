from rest_framework.viewsets import ModelViewSet
from ..serializers import TurmaSerializer
from ..models import Turma

class TurmaViewSet(ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer