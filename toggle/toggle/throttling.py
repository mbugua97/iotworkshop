from rest_framework.throttling import AnonRateThrottle

class PostRateThrottle(AnonRateThrottle):
    rate = '1/s' # Limit to 1 request per 5 seconds
    def allow_request(self, request, view):
        if request.method == 'POST':
            return super().allow_request(request, view)
        return True  # Allow other methods (GET, etc.) without throttling
