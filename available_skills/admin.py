from django.contrib import admin
from available_skills.models import AvailableSkill

@admin.register(AvailableSkill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', "category"]
    search_fields = ['name']
