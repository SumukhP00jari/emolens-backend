from django.db import models

from django.db import models

class EmotionResponse(models.Model):
    emotion = models.CharField(max_length=20, primary_key=True)
    meaning = models.TextField()
    response1 = models.TextField(null=True, blank=True)
    response2 = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'emotion_responses'
        managed = False
