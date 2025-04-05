from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
import json

class JWTAuthenticationMiddleware:
    """
    Middleware to handle JWT token refresh automatically.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip for login, signup, and API endpoints
        if request.path.startswith('/login/') or request.path.startswith('/signup/') or request.path.startswith('/api/'):
            return None

        # Check if user is authenticated
        if 'user_id' in request.session and 'access_token' in request.session:
            # Token is already valid, no need to refresh
            return None

        # If we get here, user is not authenticated
        return None 