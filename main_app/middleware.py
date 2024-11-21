from django.contrib.sessions.models import Session
from .models import Game

class GameCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if session is ending
        if not request.session.session_key:
            if request.user.is_authenticated:
                # Cleanup any unfinished games
                Game.objects.filter(
                    user=request.user,
                    result=False
                ).delete()
                
        return response
