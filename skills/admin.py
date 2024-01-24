# app1/admin.py
from django.contrib import admin
from .models import Skill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('intern', 'skill_name', 'experience_level', 'years_of_experience', 'portfolio_link')
    list_filter = ('intern', 'experience_level')
    search_fields = ('intern__intern_name', 'skill_name')
