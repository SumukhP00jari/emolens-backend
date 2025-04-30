from django.db import models

class SimulatorScenario(models.Model):
    scenario_id = models.IntegerField(primary_key=True)
    scenario_title = models.TextField()
    background = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'simulator_scenarios'
        managed = False


class SimulatorQuestion(models.Model):
    question_id = models.IntegerField(primary_key=True)
    scenario = models.ForeignKey(SimulatorScenario, on_delete=models.DO_NOTHING, db_column='scenario_id')
    round_num = models.IntegerField()
    question_text = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'simulator_questions'
        managed = False


class SimulatorAnswer(models.Model):
    answer_id = models.IntegerField(primary_key=True)
    question = models.ForeignKey(SimulatorQuestion, on_delete=models.DO_NOTHING, db_column='question_id')
    answer_text = models.TextField()
    emotion_indicate = models.CharField(max_length=20, null=True, blank=True)
    next_question_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'simulator_answers'
        managed = False
