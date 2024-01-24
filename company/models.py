# app1/models.py
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    founded_date = models.DateField()
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    headquarters = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True)
    company_timezone = models.CharField(max_length=50)  # Storing time zone as a string
    timezone_required = models.CharField(max_length=50)

    def __str__(self):
        return self.name
