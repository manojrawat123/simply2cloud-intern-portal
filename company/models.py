# app1/models.py
from django.db import models
from intern_user.models import InternUser


class Company(models.Model):
    company_user = models.ForeignKey(InternUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, unique=True)
    company_description = models.TextField(blank=True, null=True)
    founded_date = models.DateField()
    website = models.URLField()
    industry = models.CharField(max_length=100)
    headquarters = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True          )
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    company_timezone = models.CharField(max_length=50, default="UTC")
    timezone_required = models.CharField(max_length=50, default="UTC")

    def __str__(self):
        return self.company_name
