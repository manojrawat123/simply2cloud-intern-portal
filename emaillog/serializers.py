from rest_framework import serializers
from emaillog.models import EmailLog

class EmailLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = "__all__"