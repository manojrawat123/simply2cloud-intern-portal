from django.db import models
from intern_user.models import InternUser
from job_categoery.models import JobCategory
from sub_categoery.models import SubCategory
from available_skills.models import AvailableSkill

class JobExperience(models.Model):
    user = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    sub_categoery = models.ForeignKey(SubCategory, on_delete= models.CASCADE)
    job_categoery = models.ForeignKey(JobCategory,on_delete= models.CASCADE)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    skills_accuired = models.ManyToManyField(AvailableSkill)
    end_date = models.DateField(null=True, blank=True)
    desc = models.TextField()
    def __str__(self):
        return f"{self.user.email}"