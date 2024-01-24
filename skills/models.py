# app1/models.py
from django.db import models
from intern_details.models import Intern  # Assuming Intern model is in app1

class Skill(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)
    experience_level = models.IntegerField()  # Assuming a scale from 1 to 10
    years_of_experience = models.FloatField()
    portfolio_link = models.URLField()

    def __str__(self):
        return f"{self.intern.intern_name} - {self.skill_name}"
