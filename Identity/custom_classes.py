from django.core.cache import cache
from rest_framework_simplejwt.tokens import AccessToken
import secrets
import string


class CacheManager():
    @staticmethod
    def set_cache_token(user, timeout_minutes=3):
        try:
            token = AccessToken.for_user(user)
            cache_key = f"change_password_token_{user.id}"
            cache.set(cache_key, token, timeout=timeout_minutes * 60)
            return token  # You can remove this line if using the above code
        except Exception as e:
            print(f"Error setting cache token: {e}")

    @staticmethod
    def get_cache_token(user_id):
        try:
            cache_key = f"change_password_token_{user_id}"
            stored_token = cache.get(cache_key)
            return stored_token
        except Exception as e:
            print(f"Error getting cache token: {e}")
            return None

    @staticmethod
    def delete_cache_token(user):
        try:
            cache_key = f"change_password_token_{user.id}"
            cache.delete(cache_key)
            return True
        except Exception as e:
            print(f"Error deleting cache token: {e}")
            return None


class GlobalFunction:
    @staticmethod
    def make_random_password(length=6):
        """
        Generates a random password.

        Args:
            length (int): The length of the password. Default is 6.

        Returns:
            str: The randomly generated password.

        Raises:
            None
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
