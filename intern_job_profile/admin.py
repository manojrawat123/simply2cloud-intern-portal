# jobs/admin.py
from django.contrib import admin
from intern_job_profile.models import InternJobProfile

class InternJobProfileAdmin(admin.ModelAdmin):
    list_display = ('intern', 'job_categoery','title', 'expected_salary', 'experience_years', 'desc')
    search_fields = ('job_categoery', 'description')

# Register the Job model with the custom admin class
admin.site.register(InternJobProfile, InternJobProfileAdmin)
