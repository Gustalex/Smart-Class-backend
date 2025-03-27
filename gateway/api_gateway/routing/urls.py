from django.urls import path
from .routers import AuthRouter

urlpatterns = [
    path('auth/', AuthRouter.as_view(), name='auth-root'),
    path('auth/<path:path>', AuthRouter.as_view(), name='auth-proxy'),
]