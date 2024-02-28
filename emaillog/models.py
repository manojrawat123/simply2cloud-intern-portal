from django.db import models

# Create your models here.
class EmailLog(models.Model):
    title = models.CharField(max_length = 100)
    desc = models.TextField()
    company = models.ForeignKey(on_delete = models.CASCADE)
    intern_user = models.ForeignKey(on_delete = models.CASCADE)