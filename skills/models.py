# app1/models.py
from django.db import models
from intern_user.models import InternUser  # Assuming Intern model is in app1
from available_skills.models import AvailableSkill

class Skill(models.Model):
    intern = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(AvailableSkill, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)
    experience_level = models.IntegerField(default = 9) 
    years_of_experience = models.FloatField(default = 1)
    user_image = models.ImageField(upload_to='job_profiles/', null=True, blank=True)
 
    portfolio_link = models.URLField()
    def __str__(self):
        return f"{self.intern.intern_name} - {self.skill_name}"
 