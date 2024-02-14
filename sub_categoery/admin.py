from django.contrib import admin
from .models import SubCategory

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name', 'is_active', 'is_display', 'category')
    list_filter = ('is_active', 'is_display')
    search_fields = ('sub_category_name', 'category')

admin.site.register(SubCategory, SubCategoryAdmin)
