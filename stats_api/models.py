from django.db import models

class ADHD(models.Model):
    sex = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)
    rate_per_1000 = models.FloatField()

    class Meta:
        db_table = 'adhd'  # This matches the existing table in RDS
        managed = False    # Important! Since table already exists

class Neurodivergent(models.Model):
    year = models.CharField(max_length=20)
    rate_million = models.FloatField()

    class Meta:
        db_table = 'neurodivergent'
        managed = False
