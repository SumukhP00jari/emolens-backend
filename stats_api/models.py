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
    question = models.TextField(primary_key=True)
    content = models.TextField()
    data_insight = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'learning_hub'
        managed = False


class ADHDTreatment(models.Model):
    treatment_type = models.CharField(max_length=50)
    age_group = models.CharField(max_length=50)
    percentage = models.FloatField()

    class Meta:
        db_table = 'adhd_treatment'
        managed = False
        unique_together = (('treatment_type', 'age_group'),)
        


class ADHDPrevalenceYear(models.Model):
    year = models.IntegerField()
    sex = models.CharField(max_length=10)
    adhd_estimate = models.IntegerField()

    class Meta:
        db_table = 'adhd_prevalence_year'
        managed = False
        unique_together = (('year', 'sex'),)
        


class ADHDPrevalenceAge(models.Model):
    sex = models.CharField(max_length=10)
    age_group = models.CharField(max_length=20)
    adhd_estimate = models.IntegerField()

    class Meta:
        db_table = 'adhd_prevalence_age'
        managed = False
        unique_together = (('sex', 'age_group'),)


class ADHDPrescription(models.Model):
    age_group = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    count = models.IntegerField()

    class Meta:
        db_table = 'adhd_prescription'
        managed = False
        unique_together = (('age_group', 'year'),)


class ADHDDisorder(models.Model):
    mental_disorder = models.CharField(max_length=50)
    sex = models.CharField(max_length=10)
    prevalence = models.FloatField()

    class Meta:
        db_table = 'adhd_disorder'
        managed = False
        unique_together = (('mental_disorder', 'sex'),)


class ADHDCondition(models.Model):
    age_group = models.CharField(max_length=20)
    conditions = models.CharField(max_length=100)
    percentage = models.FloatField()

    class Meta:
        db_table = 'adhd_condition'
        managed = False
        unique_together = (('age_group', 'conditions'),)


class ADHDDayOff(models.Model):
    disorder = models.CharField(max_length=100, primary_key=True)
    average_days_absent = models.IntegerField()

    class Meta:
        db_table = 'adhd_dayoff'
        managed = False