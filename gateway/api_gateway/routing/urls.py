from django.urls import path
from .routers import AuthRouter, LMSRouter, AvaliacaoRouter

urlpatterns = [
    # Auth microservice routes
    path('auth/', AuthRouter.as_view(), name='auth-root'),
    path('auth/<path:path>', AuthRouter.as_view(), name='auth-proxy'),
    # LMS microservice routes
    path('lms/', LMSRouter.as_view(), name='lms-root'),
    path('lms/<path:path>', LMSRouter.as_view(), name='lms-proxy'),
    # Avaliacao microservice routes
    path('avaliacao/', AvaliacaoRouter.as_view(), name='avaliacao-root'),
    path('avaliacao/<path:path>', AvaliacaoRouter.as_view(), name='avaliacao-proxy'),
]