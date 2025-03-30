from django.urls import path 
from .views import LoginView, LogoutView, RegisterView, UserViewSet, RefreshView, VerifyRoleView, VerifyTokenView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-role/', VerifyRoleView.as_view(), name='verify-role'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify-token'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('users/', UserViewSet.as_view({'get':'list_users'}), name='users'),
    path('users/<int:pk>/', UserViewSet.as_view({'get':'retrieve_user'}), name='user'),
    path('users/<int:pk>/update/', UserViewSet.as_view({'patch':'update_user'}), name='update_user'),
    path('users/<int:pk>/delete/', UserViewSet.as_view({'delete':'delete_user'}), name='delete_user'),
]