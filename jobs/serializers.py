from rest_framework import serializers
from jobs.models import Job
from available_skills.serializer import AvailableSkillSerializer
from company.serializers import MyCompanyGetSerializer

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"


class JobGetSerializer(serializers.ModelSerializer):
    skills_required = AvailableSkillSerializer(many=True)
    skills_preferred = AvailableSkillSerializer(many=True)
    company = MyCompanyGetSerializer()
    class Meta:
        model = Job
        fields = "__all__"