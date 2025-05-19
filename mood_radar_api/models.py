from django.db import models

# Model for storing emotion-based suggestions and meanings
class EmotionResponse(models.Model):
    emotion = models.CharField(max_length=20, primary_key=True)  # e.g., "Happy", "Sad"
    meaning = models.TextField()                                 # Explanation of the emotion
    response1 = models.TextField(null=True, blank=True)          # Suggested response 1
    response2 = models.TextField(null=True, blank=True)          # Suggested response 2

    class Meta:
        db_table = 'emotion_responses'  # Name of the table in the database
        managed = False                 # Django should not manage table migration