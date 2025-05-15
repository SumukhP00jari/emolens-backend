from django.db import models


class EmotionGuessing(models.Model):
    id = models.AutoField(primary_key=True)  
    question_id = models.IntegerField()
    image_url = models.TextField(null=True)
    answer_id = models.IntegerField(null=True)
    answer_desc = models.CharField(max_length=100, null=True)
    correct_answer_id = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'emotion_guessing'
