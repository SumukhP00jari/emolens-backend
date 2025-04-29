from django.urls import path
from .views import ConversationReviewAPIView

urlpatterns = [
    path("conversation-review/", ConversationReviewAPIView.as_view(), name="conversation-review"),
]
