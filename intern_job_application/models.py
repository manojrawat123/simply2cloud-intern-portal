from django.db import models
from intern_user.models import InternUser
from jobs.models import Job
from intern_profile_job.models import InternJobProfile


class JobApplication(models.Model):
    user = models.ForeignKey(InternUser, on_delete=models.CASCADE, related_name='intern_user_related')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=[
        ("Pending", "Pending"),
        ("Accepted","Accepted"),
        ("Rejected","Rejected")
    ], default="Pending")
    intern_job_profile = models.ForeignKey(InternJobProfile, on_delete=models.CASCADE, related_name='intern_user_related')
    company_user = models.ForeignKey(InternUser, on_delete = models.CASCADE, related_name='company_user_related')
    date_applied = models.DateTimeField(auto_now_add=True)
