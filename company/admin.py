# app1/admin.py
from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_timezone', 'timezone_required')
    search_fields = ('company_name',)
