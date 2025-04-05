from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Sponsor, College

class MongoEngineBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, user_type=None):
        if not email or not password or not user_type:
            return None

        try:
            if user_type == 'sponsor':
                user = Sponsor.objects.get(email=email)
            else:
                user = College.objects.get(email=email)

            if check_password(password, user.password):
                return user
        except (Sponsor.DoesNotExist, College.DoesNotExist):
            return None

        return None

    def get_user(self, user_id):
        try:
            # Try to find the user in both collections
            try:
                return Sponsor.objects.get(id=user_id)
            except Sponsor.DoesNotExist:
                pass

            try:
                return College.objects.get(id=user_id)
            except College.DoesNotExist:
                pass

            return None
        except Exception:
            return None 