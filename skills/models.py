# app1/models.py
from django.db import models
from intern_user.models import InternUser  # Assuming Intern model is in app1

class Skill(models.Model):
    intern = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)
    experience_level = models.IntegerField() 
    years_of_experience = models.FloatField()
    portfolio_link = models.URLField()

    def __str__(self):
        return f"{self.intern.intern_name} - {self.skill_name}"
