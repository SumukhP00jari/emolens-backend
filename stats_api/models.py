from django.db import models

class ADHD(models.Model):
    sex = models.CharField(max_length=10, primary_key=True)
    age_group = models.CharField(max_length=10)
    rate_per_1000 = models.FloatField()

    class Meta:
        db_table = 'adhd'
        managed = False

class Neurodivergent(models.Model):
    year = models.CharField(max_length=20, primary_key=True)  #year is unique
    rate_million = models.FloatField()

    class Meta:
        db_table = 'neurodivergent'
        managed = False

class LearningHub(models.Model):
    title = models.TextField()
    content = models.TextField()

    class Meta:
        db_table = 'learninghub'
        managed = False

class ADHDTreatment(models.Model):
    year = models.TextField()
    treatment = models.TextField()

    class Meta:
        db_table = 'adhd_treatment'
        managed = False

class ADHDPrevalenceYear(models.Model):
    year = models.TextField()
    prevalence_rate = models.FloatField()

    class Meta:
        db_table = 'adhd_prevalence_year'
        managed = False

class ADHDPrevalenceAge(models.Model):
    age_group = models.TextField()
    prevalence_rate = models.FloatField()

    class Meta:
        db_table = 'adhd_prevalence_age'
        managed = False

class ADHDDisorder(models.Model):
    disorder_type = models.TextField()
    percent = models.FloatField()

    class Meta:
        db_table = 'adhd_disorder'
        managed = False

class ADHDCondition(models.Model):
    condition = models.TextField()
    percent = models.FloatField()

    class Meta:
        db_table = 'adhd_condition'
        managed = False

class ADHDDayOff(models.Model):
    category = models.TextField()
    percent = models.FloatField()

    class Meta:
        db_table = 'adhd_dayoff'
        managed = False

class ADHDPrescription(models.Model):
    prescription = models.TextField()
    percent = models.FloatField()

    class Meta:
        db_table = 'adhd_prescription'
        managed = False