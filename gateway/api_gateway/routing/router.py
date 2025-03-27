from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

class MicroserviceRouter(APIView):
    service_url = None 
    service_prefix = ''  

    def _proxy_request(self, request, path=''):
        try:
            base_url = self.service_url.rstrip('/')
            prefix = self.service_prefix.strip('/')
            path = path.strip('/')
            full_url = '/'.join([part for part in [base_url, prefix, path] if part]) + '/'

            headers = {
                'Content-Type': request.headers.get('Content-Type', 'application/json')
            }
            
            auth_header = request.headers.get('Authorization') or request.headers.get('Access')
            if auth_header:
                if not auth_header.startswith('Bearer '):
                    auth_header = f'Bearer {auth_header}'
                headers['Authorization'] = auth_header

            print(f"Proxying to: {full_url}")
            print(f"Headers being sent: {headers}")

            response = requests.request(
                method=request.method,
                url=full_url,
                headers=headers,
                data=request.body,
                timeout=5
            )

            return Response(
                response.json() if response.content else {},
                status=response.status_code
            )
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