class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Set X-Content-Type-Options
        response["X-Content-Type-Options"] = "nosniff"

        # Set Referrer-Policy
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Set Permissions-Policy
        response["Permissions-Policy"] = (
            "geolocation=(self), microphone=(), camera=()"
        )

        return response