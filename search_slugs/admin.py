from django.contrib import admin
from .models import SearchSlugs

class SearchSlugsAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title_slug', 'location_slug', 'company_name_slug')
    search_fields = ('job_title_slug', 'location_slug', 'company_name_slug')

admin.site.register(SearchSlugs, SearchSlugsAdmin)
