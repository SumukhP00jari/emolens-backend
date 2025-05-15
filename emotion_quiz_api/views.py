from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EmotionGuessing
from .serializers import EmotionGuessingSerializer

class EmotionGuessingAPIView(APIView):
    def get(self, request):
        data = EmotionGuessing.objects.all()
        serializer = EmotionGuessingSerializer(data, many=True)
        return Response(serializer.data)

