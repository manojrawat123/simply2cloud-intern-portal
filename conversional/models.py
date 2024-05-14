from django.db import models
from intern_user.models import InternUser

class Conversation(models.Model):
    sender = models.ForeignKey(InternUser, on_delete=models.CASCADE, related_name='sent_conversations')
    receiver = models.ForeignKey(InternUser, on_delete=models.CASCADE, related_name='received_conversations')
    last_message = models.TextField()
    unread_message_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Conversation between {self.sender} and {self.receiver}"
