# app1/models.py
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Intern(models.Model):
    intern_name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    available = models.BooleanField(default=True)
    s2c_certified = models.BooleanField(default=False)
    priority = models.IntegerField(
        validators = [
            MinValueValidator(1, message="Priority must be at least 1"),
            MaxValueValidator(10, message="Priority cannot be above 10")
        ]
    )
    def __str__(self):
        return self.intern_name
