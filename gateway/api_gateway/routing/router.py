from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
import requests

class MicroserviceRouter(APIView):
    service_url = None
    service_prefix = ''
    verify_token_url = 'http://auth-service:8000/api/auth/verify-token/'

    def _verify_token(self, request):
        """Verifica o token JWT com o Auth-Service"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None
            
        token = auth_header.split(' ')[-1] if auth_header else None
        
        try:
            response = requests.post(
                self.verify_token_url,
                json={'token': token},
                timeout=2
            )
            return response if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error verifying token: {str(e)}")
            return None

    def _proxy_request(self, request, path=''):
        user_info = None 
        
        if not path.startswith(('login/', 'register/', 'auth/')):
            auth_response = self._verify_token(request)
            if not auth_response:
                return Response(
                    {'detail': 'Token inválido ou serviço indisponível'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            user_info = auth_response.json()

        try:
            base_url = self.service_url.rstrip('/')
            prefix = self.service_prefix.strip('/')
            path = path.strip('/')
            full_url = '/'.join([part for part in [base_url, prefix, path] if part]) + '/'
            
            headers = {
                'Content-Type': request.headers.get('Content-Type', 'application/json'),
                'X-Forwarded-From-Gateway': 'true',
                'Authorization': request.headers.get('Authorization', '')
            }
            
            if user_info:
                headers.update({
                    'X-User-ID': str(user_info.get('user_id', '')),
                    'X-User-Email': user_info.get('email', ''),
                    'X-User-Is-Student': 'true' if user_info.get('is_student') else 'false',
                    'X-User-Is-Teacher': 'true' if user_info.get('is_teacher') else 'false',
                    'X-User-Is-Manager': 'true' if user_info.get('is_manager') else 'false',
                })

            print(f"Proxying to: {full_url}")

            response = requests.request(
                method=request.method,
                url=full_url,
                headers=headers,
                data=request.body,
                timeout=30, 
                stream=True
            )

            proxy_response = Response(
                content_type=response.headers.get('Content-Type'),
                status=response.status_code
            )

            if 'application/json' not in response.headers.get('Content-Type', ''):
                proxy_response = FileResponse(
                    response.raw,
                    content_type=response.headers.get('Content-Type'),
                    status=response.status_code
                )
                if 'Content-Disposition' in response.headers:
                    proxy_response['Content-Disposition'] = response.headers['Content-Disposition']
                return proxy_response

            proxy_response.data = response.json() if response.content else {}
            return proxy_response
            
        except requests.exceptions.RequestException as e:
            return Response(
                {'detail': 'Service unavailable', 'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
            
    def get(self, request, path=''):
        return self._proxy_request(request, path)
    
    def post(self, request, path=''):
        return self._proxy_request(request, path)
    
    def patch(self, request, path=''):
        return self._proxy_request(request, path)
    
    def delete(self, request, path=''):
        return self._proxy_request(request, path)