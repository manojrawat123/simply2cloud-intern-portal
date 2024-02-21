from intern_experience.models import JobExperience
from rest_framework import serializers
from job_categoery.serializer import AvailableJobCategoerySerializer
from sub_categoery.serializer import SubCategoerySerializer
from available_skills.serializer import AvailableSkillSerializer

class InternExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperience
        fields = "__all__"


class InternExperienceGetSerializer(serializers.ModelSerializer):
    job_categoery = AvailableJobCategoerySerializer()
    sub_categoery = SubCategoerySerializer()
    skills_accuired = AvailableSkillSerializer(many=True)
    class Meta:
        model = JobExperience
        fields = "__all__"
