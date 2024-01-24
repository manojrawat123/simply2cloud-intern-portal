# app1/models.py
from django.db import models
from intern_details.models import Intern  # Assuming Intern model is in app1
from company.models import Company  # Assuming Company model is in app2

class Engagement(models.Model):
    intern = models.ForeignKey(Intern, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.intern.intern_name} - {self.company.company_name} ({self.start_date} to {self.end_date})"
