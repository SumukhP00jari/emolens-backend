from django.urls import path
from .views import MoodRadarAPIView

urlpatterns = [
    path('mood-radar/', MoodRadarAPIView.as_view(), name='mood-radar'),
]