from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .google_docs_service import create_google_doc
from .serializers import GoogleDocSerializer
from django.shortcuts import render

def home(request):
    return render(request, "index.html")

class CreateGoogleDoc(APIView):
    def post(self, request):
        serializer = GoogleDocSerializer(data=request.data)
        if serializer.is_valid():
            try:
                doc_url = create_google_doc(serializer.validated_data['content'])
                return Response({"doc_url": doc_url}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
