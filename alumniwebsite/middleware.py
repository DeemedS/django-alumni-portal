from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings
from django.middleware.csrf import get_token

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
