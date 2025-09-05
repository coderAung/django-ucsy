from django.db import models

class ChatMessage(models.Model):
    sender = models.ForeignKey('Account', related_name='sent_messages',on_delete=models.CASCADE)
    receiver = models.ForeignKey('Account', related_name= 'received_messages', on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey('Account', related_name='customer_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']