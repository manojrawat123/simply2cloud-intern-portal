# app1/admin.py
from django.contrib import admin
from .models import Intern

@admin.register(Intern)
class InternAdmin(admin.ModelAdmin):
    list_display = ('intern_name', 'phone', 'email', 'available', 's2c_certified', 'priority')
    list_filter = ('available', 's2c_certified')
    search_fields = ('intern_name', 'email')
