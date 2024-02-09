# jobs/admin.py
from django.contrib import admin
from .models import JobCategory

class JobAdmin(admin.ModelAdmin):
    list_display = ('job_category', 'description','is_active')
    search_fields = ('job_category', 'description')

# Register the Job model with the custom admin class
admin.site.register(JobCategory, JobAdmin)
