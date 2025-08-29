from .models import AuditLog

class AuditMiddleware:
    """
    Middleware to log page views for GET requests.
    It skips static files to reduce noise.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.method == "GET" and not request.path.startswith('/static/'):
            # Log the page view after processing the response.
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                action='page_view',
                ip_address=request.META.get('REMOTE_ADDR'),
                path=request.path,
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
            )
        return response
