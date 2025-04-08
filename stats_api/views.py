from django.shortcuts import render

from django.db import connection
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

class DBConnectionCheck(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                tables = cursor.fetchall()
            return Response({"status": "connected", "tables": tables})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)