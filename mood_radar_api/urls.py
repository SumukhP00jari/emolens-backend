from django.urls import path
from .views import MoodRadarAPIView

urlpatterns = [
    path("detect/", MoodRadarAPIView.as_view(), name="mood-radar-detect"),
]
