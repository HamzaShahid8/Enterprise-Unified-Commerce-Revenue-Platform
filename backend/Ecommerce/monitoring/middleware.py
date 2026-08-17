import logging
import time

logger = logging.getLogger('django.request')

class RequestLoggingMiddleware:
    
    # django app chlny pr start hoga yay
    def __init__(self, get_response):
        self.get_response = get_response
        
        # har request pr run hoga yay
    def __call__(self, request):
        
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        user = request.user
        
        if user.is_authenticated:
            user_id = user.id
        else:
            user_id = 'anonymous'
            
        logger.info(
            'HTTP request completed',
            extra={
                'method': request.method,
                'path': request.path,
                'user': user_id,
                'status': response.status_code,
                'duration': round(duration, 3),
            }
        )
        
        return response