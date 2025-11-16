from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .repository.auth_repository import AuthTokenRepository

class SQLAlchemyTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Token '):
            return None

        token_str = auth_header.replace('Token ', '')
        token = AuthTokenRepository.get_by_token(token_str)

        if not token or not token.member:
            raise AuthenticationFailed("Invalid or expired token")

        return (token.member, token_str)
     