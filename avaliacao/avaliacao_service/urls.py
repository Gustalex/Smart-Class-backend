from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AvaliacaoAtividadeViewSet

router = DefaultRouter()
router.register(r'avaliacao_atividade', AvaliacaoAtividadeViewSet, basename='avaliacao_atividade')

urlpatterns = [
    path('', include(router.urls)),
]