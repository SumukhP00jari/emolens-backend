from django.shortcuts import render
from django.db import models

from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (
    ADHD, Neurodivergent, LearningHub, ADHDTreatment, ADHDDisorder,
    ADHDPrevalenceYear, ADHDPrevalenceAge, ADHDPrescription, ADHDCondition, ADHDDayOff
)
from .serializers import (
    ADHDSerializer, NeurodivergentSerializer, LearningHubSerializer, ADHDTreatmentSerializer,
    ADHDDisorderSerializer, ADHDPrevalenceYearSerializer, ADHDPrevalenceAgeSerializer,
    ADHDPrescriptionSerializer, ADHDConditionSerializer, ADHDDayOffSerializer
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

class LearningHub(models.Model):
    question = models.TextField(primary_key=True)
    content = models.TextField()
    data_insight = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'learning_hub'
        managed = False

class ADHDTreatment(models.Model):
    treatment_type = models.CharField(max_length=50, primary_key=True)
    age_group = models.CharField(max_length=50)
    percentage = models.FloatField()

    class Meta:
        db_table = 'adhd_treatment'
        managed = False

class ADHDPrevalenceYear(models.Model):
    year = models.IntegerField()
    sex = models.CharField(max_length=10)
    adhd_estimate = models.IntegerField()

    class Meta:
        db_table = 'adhd_prevalence_year'
        managed = False
        unique_together = ('year', 'sex')

class ADHDPrevalenceAge(models.Model):
    sex = models.CharField(max_length=10)
    age_group = models.CharField(max_length=20)
    adhd_estimate = models.IntegerField()

    class Meta:
        db_table = 'adhd_prevalence_age'
        managed = False
        unique_together = ('sex', 'age_group')

class ADHDPrescription(models.Model):
    age_group = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    count = models.IntegerField()

    class Meta:
        db_table = 'adhd_prescription'
        managed = False
        unique_together = ('age_group', 'year')

class ADHDDisorder(models.Model):
    mental_disorder = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    prevalence = models.FloatField()

    class Meta:
        db_table = 'adhd_disorder'
        managed = False
        unique_together = ('mental_disorder', 'sex')

class ADHDCondition(models.Model):
    age_group = models.CharField(max_length=20)
    conditions = models.CharField(max_length=100, primary_key=True)
    percentage = models.FloatField()

    class Meta:
        db_table = 'adhd_condition'
        managed = False

class ADHDDayoff(models.Model):
    disorder = models.CharField(max_length=100, primary_key=True)
    average_days_absent = models.IntegerField()

    class Meta:
        db_table = 'adhd_dayoff'
        managed = False

class DBConnectionCheck(APIView):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                tables = cursor.fetchall()
            return Response({"status": "connected", "tables": tables})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)