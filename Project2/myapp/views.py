import os
import openai
from gtts import gTTS
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Set your OpenAI API Key (replace with your actual key)
OPENAI_API_KEY="yoy open api key"
openai.api_key = OPENAI_API_KEY

class VoiceAgentAPI(APIView):
    def post(self, request):
        try:
            # Get user input text
            user_question = request.data.get('question', '')

            if not user_question:
                return Response({"error": "No question provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Process query using OpenAI GPT
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": user_question}]
            )

            # Extract AI response
            ai_response = response['choices'][0]['message']['content']

            # Convert text response to speech (TTS)
            tts = gTTS(text=ai_response, lang='en')
            audio_file = "voice_response.mp3"
            tts.save(audio_file)

            # Return the response text and audio file URL
            return Response({
                "text_response": ai_response,
                "audio_url": f"/media/{audio_file}"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
