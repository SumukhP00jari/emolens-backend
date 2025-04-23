"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from stats_api.views import (ADHDStatsAPIView, NeurodivergentStatsAPIView, LearningHubAPIView, ADHDTreatmentAPIView, ADHDDisorderAPIView,
    ADHDPrevalenceYearAPIView, ADHDPrevalenceAgeAPIView,
    ADHDPrescriptionAPIView, ADHDConditionAPIView, ADHDDayOffAPIView)
from stats_api.views import DBConnectionCheck


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('emolens_api.urls')),
    path('api/adhd/', ADHDStatsAPIView.as_view(), name='adhd-stats'),
    path('api/neurodivergent/', NeurodivergentStatsAPIView.as_view(), name='neurodivergent-stats'),
    path("api/check-db/", DBConnectionCheck.as_view(), name="check-db"),
    path("learning-hub/", LearningHubAPIView.as_view(), name="learning-hub"),
    path("adhd-treatment/", ADHDTreatmentAPIView.as_view(), name="adhd-treatment"),
    path("adhd-disorder/", ADHDDisorderAPIView.as_view(), name="adhd-disorder"),
    path("adhd-prevalence-year/", ADHDPrevalenceYearAPIView.as_view(), name="adhd-prevalence-year"),
    path("adhd-prevalence-age/", ADHDPrevalenceAgeAPIView.as_view(), name="adhd-prevalence-age"),
    path("adhd-prescription/", ADHDPrescriptionAPIView.as_view(), name="adhd-prescription"),
    path("adhd-condition/", ADHDConditionAPIView.as_view(), name="adhd-condition"),
    path("adhd-dayoff/", ADHDDayOffAPIView.as_view(), name="adhd-dayoff"),
]
