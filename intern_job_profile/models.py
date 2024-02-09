from django.db import models
from intern_user.models import InternUser
from job_categoery.models import JobCategory
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class InternJobProfile(models.Model):
    intern = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    job_categoery = models.ForeignKey(JobCategory,on_delete= models.CASCADE)
    title = models.CharField(max_length=500)
    expected_salary = models.IntegerField(
        validators=[
            MinValueValidator(5000, message='Expected salary must be at least 3000.'),
            MaxValueValidator(100000, message='Expected salary must not exceed 1 lakh.')
        ]
    )
    experience_years = models.IntegerField()
    desc = models.TextField()