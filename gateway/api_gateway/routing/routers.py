from .router import MicroserviceRouter
from api_gateway.services import auth

class AuthRouter(MicroserviceRouter):
    service_url = auth.AUTH_SERVICE_URL
    service_prefix = 'api/auth'