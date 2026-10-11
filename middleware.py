import time
from.models import APILog

class APILoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = (time.time() - start) * 1000

        try:
            if request.path.startswith('/api/'):
                APILog.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    endpoint=request.path,
                    method=request.method,
                    response_time_ms=duration,
                    status_code=response.status_code
                )
        except:
            pass
        return response