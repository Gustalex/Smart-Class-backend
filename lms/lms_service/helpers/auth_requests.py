# helpers.py
import requests

def make_request_to_auth(request, method, endpoint, data=None):
    auth_service_url = 'http://auth-service:8000' 
    url = f"{auth_service_url}/{endpoint}"
    
    headers = {
        'Authorization': request.headers.get('Authorization', ''),
        'Content-Type': 'application/json',
        'X-Forwarded-From-Gateway': 'true',
        'X-User-ID': str(request.user.id),
        'X-User-Email': getattr(request.user, 'email', '')
    }
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            timeout=5
        )
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request to auth service: {str(e)}")
        return None