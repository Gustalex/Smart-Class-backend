from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecomendacaoViewSet

router = DefaultRouter()
router.register(r'recomendacao', RecomendacaoViewSet, basename='recomendacao')

urlpatterns = [
    path('', include(router.urls)),
]