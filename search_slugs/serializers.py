from rest_framework import serializers
from search_slugs.models import SearchSlugs

class SearchSlugSerializers(serializers.ModelSerializer):
    class Meta:
        model = SearchSlugs
        fields = "__all__"