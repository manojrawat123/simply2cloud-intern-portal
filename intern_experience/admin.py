from django.contrib import admin
from intern_experience.models import JobExperience

class JobExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'start_date', 'end_date')

admin.site.register(JobExperience, JobExperienceAdmin)