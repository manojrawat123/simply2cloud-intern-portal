from rest_framework import serializers
from sub_categoery.models import SubCategory

class SubCategoerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"
        