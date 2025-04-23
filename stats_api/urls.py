from django.urls import path
from .views import (
    LearningHubAPIView, ADHDTreatmentAPIView, ADHDDisorderAPIView,
    ADHDPrevalenceYearAPIView, ADHDPrevalenceAgeAPIView, ADHDPrescriptionAPIView,
    ADHDConditionAPIView, ADHDDayOffAPIView
)

urlpatterns = [
    path("learning-hub/", LearningHubAPIView.as_view(), name="learning-hub"),
    path("adhd-treatment/", ADHDTreatmentAPIView.as_view(), name="adhd-treatment"),
    path("adhd-disorder/", ADHDDisorderAPIView.as_view(), name="adhd-disorder"),
    path("adhd-prevalence-year/", ADHDPrevalenceYearAPIView.as_view(), name="adhd-prevalence-year"),
    path("adhd-prevalence-age/", ADHDPrevalenceAgeAPIView.as_view(), name="adhd-prevalence-age"),
    path("adhd-prescription/", ADHDPrescriptionAPIView.as_view(), name="adhd-prescription"),
    path("adhd-condition/", ADHDConditionAPIView.as_view(), name="adhd-condition"),
    path("adhd-dayoff/", ADHDDayOffAPIView.as_view(), name="adhd-dayoff"),
]
