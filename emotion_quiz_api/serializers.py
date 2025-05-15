from rest_framework import serializers
from .models import EmotionGuessing

class EmotionGuessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionGuessing
        fields = '__all__'
