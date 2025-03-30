from .router import MicroserviceRouter
from api_gateway.services import auth, lms

class AuthRouter(MicroserviceRouter):
    service_url = auth.AUTH_SERVICE_URL
    service_prefix = 'api/auth'


class LMSRouter(MicroserviceRouter):
    service_url = lms.LMS_SERVICE_URL
    service_prefix = 'api/lms'