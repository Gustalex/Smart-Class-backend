from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class GatewayJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if 'X-Forwarded-From-Gateway' in request.headers:
            user_id = request.headers.get('X-User-ID')
            if not user_id:
                raise AuthenticationFailed('User not found', code='user_not_found')
            
            from django.contrib.auth.models import AnonymousUser
            user = AnonymousUser()
            user.id = int(user_id)
            user.email = request.headers.get('X-User-Email', '')
            user.is_student = request.headers.get('X-User-Is-Student', 'false').lower() == 'true'
            user.is_teacher = request.headers.get('X-User-Is-Teacher', 'false').lower() == 'true'
            user.is_manager = request.headers.get('X-User-Is-Manager', 'false').lower() == 'true'
            user.access_token = request.headers.get('Authorization', '').split(' ')[-1]
            
            return (user, None)
        
        return super().authenticate(request)