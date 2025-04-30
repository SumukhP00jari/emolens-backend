from django.urls import path
from simulator_api.views import (
    ScenarioListAPIView,
    ScenarioStartAPIView,
    NextRoundAPIView
)

urlpatterns = [
    path('', ScenarioListAPIView.as_view(), name='scenario-list'),
    path('<int:scenario_id>/', ScenarioStartAPIView.as_view(), name='scenario-start'),
    path('next/', NextRoundAPIView.as_view(), name='next-question'),
]

