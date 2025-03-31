from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CursoViewSet, TurmaViewSet, AulaViewSet, AtividadeViewSet

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'turmas', TurmaViewSet, basename='turma')
router.register(r'aulas', AulaViewSet, basename='aula')
router.register(r'atividades', AtividadeViewSet, basename='atividade')

urlpatterns = [
    path('', include(router.urls)),
]
