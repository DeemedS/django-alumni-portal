from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model
import jwt
import requests

class HttpOnlyCSRFMiddleware(CsrfViewMiddleware):
    def _set_token(self, request, response):
        token = get_token(request)
        if getattr(response, 'csrf_cookie_set', False):
            return
        response.set_cookie(
            settings.CSRF_COOKIE_NAME,
            token,
            max_age=settings.CSRF_COOKIE_AGE,
            domain=None,
            path='/',
            secure=True,
            httponly=True,
            samesite=settings.CSRF_COOKIE_SAMESITE,
        )
        response.csrf_cookie_set = True

def init_csp_nonce_middleware(get_response):
    def middleware(request):
        str(getattr(request, "csp_nonce", None))
        return get_response(request)

    return middleware

class RemoveServerHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Clean headers
        response.headers.pop('Server', None)
        response.headers.pop('X-Powered-By', None)
        return response
    
class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        request.is_user_authenticated = False
        request.is_admin = False

        user_agent = request.META.get('HTTP_USER_AGENT', 'Mozilla/5.0')

        base_headers = {
            'User-Agent': user_agent
        }

        if access_token and refresh_token:
            try:
                api_url = f"{settings.API_TOKEN_URL}/token/verify/"
                response = requests.post(api_url, data={'token': access_token}, headers=base_headers)

                if response.status_code == 200:
                    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
                    user_id = payload.get("user_id")

                    if user_id:
                        User = get_user_model()
                        try:
                            request.is_user_authenticated = True
                        except User.DoesNotExist:
                            pass
            except Exception:
                pass
