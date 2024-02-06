from rest_framework import serializers
from available_skills.models import AvailableSkill

class AvailableSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSkill
        fields = "__all__"