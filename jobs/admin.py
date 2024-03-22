from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('company', 'location', 'job_commute_type', 'posted_at', 'is_active')
    search_fields = ('company__name', 'location')
    list_filter = ('job_commute_type', 'is_active', 'posted_at')
    date_hierarchy = 'posted_at'
    ordering = ('-posted_at',)
