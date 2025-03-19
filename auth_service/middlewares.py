# auth_service/middlewares.py
import jwt
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Exclude paths that don't need authentication
        exempt_paths = ['/api/login/', '/api/register/', '/admin/']
        if any(request.path.startswith(path) for path in exempt_paths):
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Authentication token required'}, status=401)
        
        token = auth_header.split(' ')[1]
        
        # Check token in cache
        cache_key = f'jwt_token_{token}'
        user_id = cache.get(cache_key)
        
        if not user_id:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = payload['user_id']
                
                # Cache the decoded token
                cache.set(cache_key, user_id, 3600)  # Cache for 1 hour
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        
        # Add user to request
        request.user_id = user_id
        
        return self.get_response(request)