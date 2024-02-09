from rest_framework import serializers
from job_categoery.models import JobCategory

class AvailableJobCategoerySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = "__all__"