from django.db import models

class ADHD(models.Model):
    sex = models.CharField(max_length=10, primary_key=True)
    age_group = models.CharField(max_length=10)
    rate_per_1000 = models.FloatField()

    class Meta:
        db_table = 'adhd'
        managed = False

class Neurodivergent(models.Model):
    year = models.CharField(max_length=20, primary_key=True)  
    rate_million = models.FloatField()

    class Meta:
        db_table = 'neurodivergent'
        managed = False

class LearningHub(models.Model):
    question = models.TextField()
    content = models.TextField()
    data_insight = models.TextField()

    class Meta:
        db_table = 'learning_hub'
        managed = False
        default_auto_field = None  

class ADHDTreatment(models.Model):
    treatment_type = models.TextField()
    age_group = models.TextField()
    percentage = models.FloatField()

    class Meta:
        db_table = 'adhd_treatment'
        managed = False
        default_auto_field = None

class ADHDPrevalenceYear(models.Model):
    year = models.CharField(max_length=10)
    sex = models.TextField()
    adhd_estimate = models.IntegerField()

    class Meta:
        db_table = 'adhd_prevalence_year'
        managed = False
        default_auto_field = None

class ADHDPrevalenceAge(models.Model):
    sex = models.CharField(max_length=20)
    age_group = models.CharField(max_length=10)
    adhd_estimate = models.IntegerField()

    class Meta:
        db_table = 'adhd_prevalence_age'
        managed = False
        default_auto_field = None

class ADHDDisorder(models.Model):
    mental_disorder = models.TextField()
    sex = models.TextField()
    prevalence = models.FloatField()

    class Meta:
        db_table = 'adhd_disorder'
        managed = False
        default_auto_field = None

class ADHDCondition(models.Model):
    age_group = models.TextField()
    conditions = models.TextField()
    percentage = models.FloatField()

    class Meta:
        db_table = 'adhd_condition'
        managed = False
        default_auto_field = None

class ADHDDayOff(models.Model):
    disorder = models.TextField()
    average_days_absent = models.IntegerField()

    class Meta:
        db_table = 'adhd_dayoff'
        managed = False
        default_auto_field = None

class ADHDPrescription(models.Model):
    age_group = models.TextField()
    year = models.TextField()
    count = models.IntegerField()

    class Meta:
        db_table = 'adhd_prescription'
        managed = False
        default_auto_field = None