from django.urls import path
from .views import RephraseTextAPIView

urlpatterns = [
    path('rewrite/', RephraseTextAPIView.as_view(), name='rewrite-text'),
]
