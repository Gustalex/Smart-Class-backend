from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CursoViewSet, TurmaViewSet

router = DefaultRouter()
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'turmas', TurmaViewSet, basename='turma')

urlpatterns = [
    path('', include(router.urls)),
]
