from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ADHD, Neurodivergent
from .serializers import ADHDSerializer, NeurodivergentSerializer

class ADHDStatsAPIView(APIView):
    def get(self, request):
        data = ADHD.objects.all()
        serializer = ADHDSerializer(data, many=True)
        return Response(serializer.data)

class NeurodivergentStatsAPIView(APIView):
    def get(self, request):
        data = Neurodivergent.objects.all()
        serializer = NeurodivergentSerializer(data, many=True)
        return Response(serializer.data)

