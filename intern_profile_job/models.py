from django.db import models
from intern_user.models import InternUser
from job_categoery.models import JobCategory
from sub_categoery.models import SubCategory
from django.core.validators import MinValueValidator, MaxValueValidator
from skills.models import Skill 
from available_skills.models import AvailableSkill 
from intern_experience.models import JobExperience

# Create your models here.
class InternJobProfile(models.Model):
    intern = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    sub_categoery = models.ForeignKey(SubCategory, on_delete= models.CASCADE)
    job_categoery = models.ForeignKey(JobCategory,on_delete= models.CASCADE)
    experience_years = models.IntegerField()
    experience = models.ManyToManyField(JobExperience,blank=True)
    desc = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    available_skills = models.ManyToManyField(AvailableSkill, blank=True)
    portfolio_link = models.URLField(null=True, blank=True)
    short_desc = models.TextField(null= True, blank=True)
    linkedin_profile = models.URLField(null=True, blank=True)
    github_profile = models.URLField(null=True, blank=True)
    thumbnail_image = models.ImageField(upload_to='job_profiles/', null=True, blank=True)
    user_image = models.ImageField(upload_to='job_profiles/', null=True, blank=True)

