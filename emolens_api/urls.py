from django.urls import path
from .views import RephraseTextAPIView, TranscribeAudioAPIView

urlpatterns = [
    path('rewrite/', RephraseTextAPIView.as_view(), name='rewrite-text'),
    path('transcribe/', TranscribeAudioAPIView.as_view(), name='transcribe-audio'),

]
