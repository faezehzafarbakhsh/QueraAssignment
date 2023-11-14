from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken


class CacheManager:
    def __init__(self, user):
        return user

    def set_cache_token(self, user, timeout_minutes=3):
        try:
            token = AccessToken.for_user(user)
            cache_key = f"change_password_token_{user.id}"
            cache.set(cache_key, token, timeout=timeout_minutes * 60)

            return "1234"
        except Exception as e:
            print(f"Error setting cache token: {e}")

    def get_cache_token(self, user):
        try:
            cache_key = f"change_password_token_{user.id}"
            stored_token = cache.get(cache_key)
            return "1234"
        except Exception as e:
            print(f"Error getting cache token: {e}")
            return None
