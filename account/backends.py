import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 2:
            prefix = auth_header[0].decode('utf8')
            token = auth_header[1].decode('utf8')
            if prefix.lower() == auth_header_prefix:
                return self._authenticate_credentials(request, token)
        return None

    def _authenticate_credentials(sef, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except:
            msg = 'Invaid auth. Cloud not decode token.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'No user matching this token was found'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'This user has been deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)