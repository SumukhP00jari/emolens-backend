from django.db import models

class ADHD(models.Model):
    sex = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)
    rate_per_1000 = models.FloatField()

    class Meta:
        db_table = 'adhd'

class Neurodivergent(models.Model):
    year = models.CharField(max_length=10)
    rate_million = models.FloatField()

    class Meta:
        db_table = 'neurodivergent'
