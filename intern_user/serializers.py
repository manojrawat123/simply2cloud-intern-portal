from rest_framework import serializers
from intern_user.models import InternUser
from django.contrib.auth.hashers import make_password

class MyUserSerializers(serializers.ModelSerializer):
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
    
    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.password = make_password(password)
        instance.save()
        return instance

class MyUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternUser
        fields = "__all__"   

    
class MyUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 225)
    class Meta:
        model = InternUser
        fields = ["email", "password"]

    def validate(self, data):
        for field_name, value in data.items():
            if value == "":
                raise serializers.ValidationError(f"{field_name} field is required.")
        return data
    

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = InternUser
    fields = "__all__"



class InternUserDetailCompanyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternUser
        fields = ["id","name", "address"]

class InternAuthCompanyUserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternUser
        fields = ["id","name","email", "phone", "address"]

# Z6SAGCK6X5V2Y6P72AF14ZAM
