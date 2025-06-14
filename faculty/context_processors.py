def custom_auth_flags(request):
    return {
        'is_user_authenticated': getattr(request, 'is_user_authenticated', False),
    }