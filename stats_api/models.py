from django.db import models

class ADHD(models.Model):
    sex = models.CharField(max_length=10)
    age_group = models.CharField(max_length=10)
    rate_per_1000 = models.FloatField()

    class Meta:
        db_table = 'adhd'
        managed = False  # <== Important: Do not try to manage this table (since it's from an existing DB)

class Neurodivergent(models.Model):
    year = models.CharField(max_length=20, primary_key=True)  # Assuming year is unique
    rate_million = models.FloatField()

    class Meta:
        db_table = 'neurodivergent'
        managed = False
