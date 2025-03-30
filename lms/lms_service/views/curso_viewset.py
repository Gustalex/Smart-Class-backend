from rest_framework.viewsets import ModelViewSet
from ..serializers import CursoSerializer
from ..models import Curso



class CursoViewSet(ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
