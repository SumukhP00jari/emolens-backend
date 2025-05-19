from django.db import models

# ADHD diagnosis rates by sex and age group
class ADHD(models.Model):
    sex = models.CharField(max_length=10, primary_key=True)
    age_group = models.CharField(max_length=10)
    rate_per_1000 = models.FloatField()

    class Meta:
        db_table = 'adhd'
        managed = False

# Neurodivergent rates per year
class Neurodivergent(models.Model):
    year = models.CharField(max_length=20, primary_key=True)
    rate_million = models.FloatField()

    class Meta:
        db_table = 'neurodivergent'
        managed = False

# Flashcards or Q&A content for the Learning Hub
class LearningHub(models.Model):
    question = models.TextField(primary_key=True)
    content = models.TextField(null=True)
    data_insight = models.TextField(null=True)

    class Meta:
        db_table = 'learning_hub'
        managed = False

# Types of ADHD treatments by age group
class AdhdTreatment(models.Model):
    treatment_type = models.CharField(max_length=100, primary_key=True)
    age_group = models.CharField(max_length=20, null=True)
    percentage = models.DecimalField(max_digits=4, decimal_places=1, null=True)

    class Meta:
        db_table = 'adhd_treatment'
        managed = False

# ADHD prevalence over years, segmented by sex
class AdhdPrevalenceYear(models.Model):
    year = models.IntegerField(primary_key=True)
    sex = models.CharField(max_length=10, null=True)
    adhd_estimate = models.IntegerField(null=True)

    class Meta:
        db_table = 'adhd_prevalence_year'
        managed = False

# ADHD prevalence across different age groups
class AdhdPrevalenceAge(models.Model):
    sex = models.CharField(max_length=10, primary_key=True)
    age_group = models.CharField(max_length=10, null=True)
    adhd_estimate = models.IntegerField(null=True)

    class Meta:
        db_table = 'adhd_prevalence_age'
        managed = False

# Prescription data for ADHD by age and year
class AdhdPrescription(models.Model):
    age_group = models.CharField(max_length=50, primary_key=True)
    year = models.CharField(max_length=9, null=True)
    count = models.IntegerField(null=True)

    class Meta:
        db_table = 'adhd_prescription'
        managed = False

# Prevalence of mental disorders related to ADHD
class AdhdDisorder(models.Model):
    mental_disorder = models.CharField(max_length=50, primary_key=True)
    sex = models.CharField(max_length=10, null=True)
    prevalence = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        db_table = 'adhd_disorder'
        managed = False

# Average days off due to different mental disorders
class AdhdDayoff(models.Model):
    disorder = models.CharField(max_length=50, primary_key=True)
    average_days_absent = models.IntegerField(null=True)

    class Meta:
        db_table = 'adhd_dayoff'
        managed = False

# Co-occurring conditions with ADHD and their percentages
class AdhdCondition(models.Model):
    age_group = models.CharField(max_length=50, primary_key=True)
    conditions = models.CharField(max_length=100, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=1, null=True)

    class Meta:
        db_table = 'adhd_condition'
        managed = False
