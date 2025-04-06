from .router import MicroserviceRouter
from api_gateway.services import auth, lms, avaliacao, recomendacao

class AuthRouter(MicroserviceRouter):
    service_url = auth.AUTH_SERVICE_URL
    service_prefix = 'api/auth'


class LMSRouter(MicroserviceRouter):
    service_url = lms.LMS_SERVICE_URL
    service_prefix = 'api/lms'


class AvaliacaoRouter(MicroserviceRouter):
    service_url = avaliacao.AVALIACAO_SERVICE_URL
    service_prefix = 'api/avaliacao'


class RecomendacaoRouter(MicroserviceRouter):
    service_url = recomendacao.RECOMENDACAO_SERVICE_URL
    service_prefix = 'api/recomendacao'