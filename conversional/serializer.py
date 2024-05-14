from rest_framework import serializers
from conversional.models import Conversation
from message.serializers import MessageSerializer
from intern_user.serializers import MyUserRegisterSerializer

class ConversionalSerializer(serializers.ModelSerializer):     
    class Meta:
        model = Conversation
        fields = "__all__"


class ConversionalGetSerializer(serializers.ModelSerializer):
    sender = MyUserRegisterSerializer()
    receiver = MyUserRegisterSerializer()
    class Meta:
        model = Conversation
        fields = "__all__"