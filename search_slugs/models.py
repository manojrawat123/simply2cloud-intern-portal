from django.db import models

# Create your models here.
class SearchSlugs(models.Model):
    job_title_slug = models.CharField(max_length = 5000,unique=True, blank=True, null=True)
    location_slug = models.CharField(max_length = 5000,unique=True, blank = True, null = True)
    company_name_slug = models.CharField(max_length=5000,unique=True, blank = True, null=True)