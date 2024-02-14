# app1/admin.py
from django.contrib import admin
from intern_user.models import InternUser

@admin.register(InternUser)
class InternAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 's2c_certified', 'priority', "user_type")
    list_filter = ('available', 's2c_certified')
    search_fields = ('email',)
