from django.urls import path
from .views import KindnessTaskAPIView

urlpatterns = [
    path('friendship-builder/', KindnessTaskAPIView.as_view(), name='friendship-builder'),
]
