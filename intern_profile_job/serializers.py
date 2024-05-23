
from rest_framework import serializers 
from intern_profile_job.models import InternJobProfile
from job_categoery.serializer import AvailableJobCategoerySerializer
from sub_categoery.serializer import SubCategoerySerializer
from intern_user.serializers import InternUserDetailCompanyViewSerializer , InternAuthCompanyUserViewSerializer
from skills.serializer import SkillsSerializer
from intern_experience.serializers import InternExperienceGetSerializer


class InternJobProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternJobProfile
        fields = "__all__"

class InternJobProfileGetSerializer(serializers.ModelSerializer):
    job_categoery = AvailableJobCategoerySerializer()
    class Meta:
        model = InternJobProfile
        fields = "__all__"

class InternUserJobProfileForCompanViewSerializer(serializers.ModelSerializer):
    experience = InternExperienceGetSerializer(many=True)
    job_categoery = AvailableJobCategoerySerializer()
    intern = InternUserDetailCompanyViewSerializer()
    skills = SkillsSerializer(many=True)
    sub_categoery = SubCategoerySerializer()
    class Meta:
        model = InternJobProfile
        exclude = ['portfolio_link', 'linkedin_profile']

class InternAuthenticatedCompanyProfileCompanyViewSerializer(serializers.ModelSerializer):
    experience = InternExperienceGetSerializer(many=True)
    job_categoery = AvailableJobCategoerySerializer()
    sub_categoery = SubCategoerySerializer()
    intern = InternAuthCompanyUserViewSerializer()
    skills = SkillsSerializer(many=True)
    class Meta:
        model = InternJobProfile
        fields = "__all__"
    
