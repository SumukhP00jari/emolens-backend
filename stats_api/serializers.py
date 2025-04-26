from rest_framework import serializers
from .models import (
    ADHD, Neurodivergent, LearningHub, ADHDTreatment,
    ADHDPrevalenceYear, ADHDPrevalenceAge,
    ADHDPrescription, ADHDDisorder, ADHDCondition, ADHDDayOff
)
class ADHDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHD
        fields = '__all__'

class NeurodivergentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neurodivergent
        fields = '__all__'

class ADHDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHD
        fields = ['sex', 'age_group', 'rate_per_1000']


class NeurodivergentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neurodivergent
        fields = ['year', 'rate_million']


class LearningHubSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningHub
        fields = ['question', 'content', 'data_insight']


class ADHDTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDTreatment
        fields = ['treatment_type', 'age_group', 'percentage']


class ADHDPrevalenceYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDPrevalenceYear
        fields = ['year', 'sex', 'adhd_estimate']


class ADHDPrevalenceAgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDPrevalenceAge
        fields = ['sex', 'age_group', 'adhd_estimate']


class ADHDDisorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDDisorder
        fields = ['mental_disorder', 'sex', 'prevalence']


class ADHDConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDCondition
        fields = ['age_group', 'conditions', 'percentage']


class ADHDDayOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDDayOff
        fields = ['disorder', 'average_days_absent']


class ADHDPrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADHDPrescription
        fields = ['age_group', 'year', 'count']