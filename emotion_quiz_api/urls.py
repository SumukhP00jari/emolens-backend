from django.urls import path
from .views import EmotionGuessingAPIView

urlpatterns = [
    path('emotion-guessing/', EmotionGuessingAPIView.as_view(), name='emotion-guessing'),
]
