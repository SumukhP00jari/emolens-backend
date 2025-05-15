from django.db import models

class EmotionGuessing(models.Model):
    question_id = models.IntegerField()
    image_url = models.TextField()
    answer_id = models.IntegerField()
    answer_desc = models.CharField(max_length=100)
    correct_answer_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'emotion_guessing'
        unique_together = (('question_id', 'answer_id'),)
