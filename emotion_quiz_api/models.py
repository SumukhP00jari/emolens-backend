from django.db import models


from django.db import models

class EmotionGuessing(models.Model):
    question_id = models.IntegerField()
    image_url = models.TextField()
    answer_id = models.IntegerField()
    answer_desc = models.CharField(max_length=100)
    correct_answer_id = models.IntegerField()

    class Meta:
        managed = False  # Because this table already exists in your DB
        db_table = 'emotion_guessing'
