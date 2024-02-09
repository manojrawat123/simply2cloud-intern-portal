from rest_framework import serializers 
from intern_job_profile.models import InternJobProfile
from job_categoery.serializer import AvailableJobCategoerySerializer
from intern_user.serializers import InternUserJobProfileForCompanViewSerializer 

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
    job_categoery = AvailableJobCategoerySerializer()
    intern = InternUserJobProfileForCompanViewSerializer()
    class Meta:
        model = InternJobProfile
        fields = "__all__"