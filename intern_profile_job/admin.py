# jobs/admin.py
from django.contrib import admin
from intern_profile_job.models import InternJobProfile

class InternJobProfileAdmin(admin.ModelAdmin):
    list_display = ('job_categoery', 'experience_years', 'desc')
    search_fields = ('job_categoery', 'description')

# Register the Job model with the custom admin class
admin.site.register(InternJobProfile, InternJobProfileAdmin)
