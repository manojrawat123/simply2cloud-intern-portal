from django.db import models
from job_categoery.models import JobCategory


class SubCategory(models.Model):
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    sub_category_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_display = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_category_name