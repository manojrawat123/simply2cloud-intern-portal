from django.db import models
from intern_user.models import InternUser
from conversional.models import Conversation

class Message(models.Model):
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="conversiation")
    sender = models.ForeignKey(InternUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(InternUser, on_delete=models.CASCADE, related_name='received_messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"
