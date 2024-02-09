from django.contrib import admin
from .models import JobApplication

class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'user', 'status', 'date_applied')
    list_filter = ('status', 'date_applied')
    search_fields = ('date_applied', 'user')  # Update these fields based on your actual model

admin.site.register(JobApplication, JobApplicationAdmin)