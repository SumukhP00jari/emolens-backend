from django.db import models



class KindnessTask(models.Model):
    task_title = models.TextField(blank=True,primary_key=True)
    task_description = models.TextField(null=True, blank=True)  

    class Meta:
        managed = False  
        db_table = 'kindness_tasks'
