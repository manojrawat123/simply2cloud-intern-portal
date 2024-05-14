from django.db import models
from intern_user.models import InternUser
from company.models import Company
from available_skills.models import AvailableSkill
from job_categoery.models import JobCategory 
from sub_categoery.models import SubCategory

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_categoery = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    sub_categoery = models.ForeignKey(SubCategory, on_delete= models.CASCADE, default=1)
    # job_title = models.CharField(max_length=255)
    company_user = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    skills_required = models.ManyToManyField(AvailableSkill, related_name='skills_required')
    skills_preferred = models.ManyToManyField(AvailableSkill, related_name='skills_preffered')
    # salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    experience = models.CharField(max_length=255)
    education = models.CharField(max_length=255)
    student_hired = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
    job_commute_type = models.CharField(max_length=50, choices=[
        ('remote', 'remote'),
        ('work_from_home', 'work_from_home'),
        ('both', 'both'),
    ])
    timezone_required = models.CharField(max_length=255)
    # Additional Fields
    responsibilities = models.TextField(blank=True, null=True)
    qualifications = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
