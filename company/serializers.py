from rest_framework import serializers
from intern_user.models import InternUser
from intern_user.serializers import MyUserRegisterSerializer
from company.models import Company

class MyCompanyUserSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only = True)
    class Meta:
        model = InternUser
        fields = ["email","name", "phone", "password", "password2", "s2c_certified"]
        extra_kwargs = {
            'password':{'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        if password != password2:
            raise serializers.ValidationError("Password Didn't match")
        return attrs
    
    def create(self, validate_data):
        validate_data.pop('password2')
        return InternUser.objects.create_user(**validate_data)

class MyCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company 
        fields = "__all__"

class MyCompanyGetSerializer(serializers.ModelSerializer):
    company_user = MyUserRegisterSerializer()
    class Meta:
        model = Company
        fields = "__all__"
    

# class MyCompanyNormalSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InternUser
#         fields = "__all__"   

    
# class MyCompanyLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length = 225)
#     class Meta:
#         model = InternUser
#         fields = ["email", "password"]

#     def validate(self, data):
#         for field_name, value in data.items():
#             if value == "":
#                 raise serializers.ValidationError(f"{field_name} field is required.")
#         return data
    
    
    