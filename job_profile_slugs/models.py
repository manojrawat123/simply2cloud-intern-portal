from django.db import models
from django.utils.text import slugify

class JobProfileSlug(models.Model):
    profile_name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)