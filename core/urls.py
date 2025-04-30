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
from stats_api.views import (
    ADHDStatsAPIView, NeurodivergentStatsAPIView, DBConnectionCheck,
     LearningHubAPIView,
    AdhdTreatmentAPIView,
    AdhdPrevalenceYearAPIView,
    AdhdPrevalenceAgeAPIView,
    AdhdPrescriptionAPIView,
    AdhdDisorderAPIView,
    AdhdConditionAPIView,
    AdhdDayoffAPIView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("emolens_api.urls")),

    path("api/adhd/", ADHDStatsAPIView.as_view(), name="adhd-stats"),
    path("api/neurodivergent/", NeurodivergentStatsAPIView.as_view(), name="neurodivergent-stats"),
    path("api/check-db/", DBConnectionCheck.as_view(), name="check-db"),


    path('api/learning-hub/', LearningHubAPIView.as_view(), name='learning-hub'),
    path('api/adhd-treatment/', AdhdTreatmentAPIView.as_view(), name='adhd-treatment'),
    path('api/adhd-prevalence-year/', AdhdPrevalenceYearAPIView.as_view(), name='adhd-prevalence-year'),
    path('api/adhd-prevalence-age/', AdhdPrevalenceAgeAPIView.as_view(), name='adhd-prevalence-age'),
    path('api/adhd-prescription/', AdhdPrescriptionAPIView.as_view(), name='adhd-prescription'),
    path('api/adhd-disorder/', AdhdDisorderAPIView.as_view(), name='adhd-disorder'),
    path('api/adhd-condition/', AdhdConditionAPIView.as_view(), name='adhd-condition'),
    path('api/adhd-dayoff/', AdhdDayoffAPIView.as_view(), name='adhd-dayoff'),

    path("api/", include("rate_api.urls")),

    path('api/simulator/', include('simulator_api.urls')),

]
