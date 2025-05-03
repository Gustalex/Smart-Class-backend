from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class AuthenticatedAnonymousUser(AnonymousUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_authenticated = False

    @property
    def is_authenticated(self):
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, value):
        self._is_authenticated = value

class GatewayJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if request.method == 'GET' and ('/cursos/' in request.path or request.path.endswith('/cursos')):
            return None
            
        if 'X-Forwarded-From-Gateway' in request.headers:
            user_id = request.headers.get('X-User-ID')
            if not user_id:
                raise AuthenticationFailed('User ID não encontrado nos headers', code='missing_user_id')
            
            user = AuthenticatedAnonymousUser()
            user.id = int(user_id)
            user.email = request.headers.get('X-User-Email', '')
            user.is_authenticated = True 
            user.is_student = request.headers.get('X-User-Is-Student', 'false').lower() == 'true'
            user.is_teacher = request.headers.get('X-User-Is-Teacher', 'false').lower() == 'true'
            user.is_manager = request.headers.get('X-User-Is-Manager', 'false').lower() == 'true'
            
            return (user, None)
        
        return super().authenticate(request)