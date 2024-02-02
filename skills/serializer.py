from rest_framework import serializers
from skills.models import Skill

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        