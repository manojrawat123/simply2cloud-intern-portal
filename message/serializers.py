from rest_framework import serializers
from message.models import Message
from intern_user.serializers import MyUserRegisterSerializer

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class MessageGetSerializer(serializers.ModelSerializer):
    sender = MyUserRegisterSerializer()
    receiver = MyUserRegisterSerializer()
    class Meta:
        model = Message
        fields = "__all__"
