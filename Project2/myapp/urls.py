from django.urls import path
from .views import VoiceAgentAPI

urlpatterns = [
    path('ask/', VoiceAgentAPI.as_view(), name="voice-agent-api"),
]
