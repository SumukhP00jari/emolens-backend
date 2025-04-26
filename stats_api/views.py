from django.shortcuts import render

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    ADHD, Neurodivergent, LearningHub, AdhdTreatment, AdhdPrevalenceYear, AdhdPrevalenceAge,
    AdhdPrescription, AdhdDisorder, AdhdCondition, AdhdDayoff
)
from .serializers import (
    ADHDSerializer, NeurodivergentSerializer, LearningHubSerializer, AdhdTreatmentSerializer, AdhdPrevalenceYearSerializer,
    AdhdPrevalenceAgeSerializer, AdhdPrescriptionSerializer, AdhdDisorderSerializer,
    AdhdConditionSerializer, AdhdDayoffSerializer
)

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
    
class LearningHubAPIView(APIView):
    def get(self, request):
        data = LearningHub.objects.all()
        serializer = LearningHubSerializer(data, many=True)
        return Response(serializer.data)

class AdhdTreatmentAPIView(APIView):
    def get(self, request):
        data = AdhdTreatment.objects.all()
        serializer = AdhdTreatmentSerializer(data, many=True)
        return Response(serializer.data)

class AdhdPrevalenceYearAPIView(APIView):
    def get(self, request):
        data = AdhdPrevalenceYear.objects.all()
        serializer = AdhdPrevalenceYearSerializer(data, many=True)
        return Response(serializer.data)

class AdhdPrevalenceAgeAPIView(APIView):
    def get(self, request):
        data = AdhdPrevalenceAge.objects.all()
        serializer = AdhdPrevalenceAgeSerializer(data, many=True)
        return Response(serializer.data)

class AdhdPrescriptionAPIView(APIView):
    def get(self, request):
        data = AdhdPrescription.objects.all()
        serializer = AdhdPrescriptionSerializer(data, many=True)
        return Response(serializer.data)

class AdhdDisorderAPIView(APIView):
    def get(self, request):
        data = AdhdDisorder.objects.all()
        serializer = AdhdDisorderSerializer(data, many=True)
        return Response(serializer.data)

class AdhdConditionAPIView(APIView):
    def get(self, request):
        data = AdhdCondition.objects.all()
        serializer = AdhdConditionSerializer(data, many=True)
        return Response(serializer.data)

class AdhdDayoffAPIView(APIView):
    def get(self, request):
        data = AdhdDayoff.objects.all()
        serializer = AdhdDayoffSerializer(data, many=True)
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