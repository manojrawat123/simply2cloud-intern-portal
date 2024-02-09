# job_category/models.py
from django.db import models

class JobCategory(models.Model):
    job_category = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    display = models.BooleanField(default = True)

    def __str__(self):
        return self.job_category

    class Meta:
        verbose_name_plural = "Job Categories"