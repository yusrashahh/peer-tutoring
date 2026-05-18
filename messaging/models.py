from django.db import models
from django.conf import settings
from django.utils import timezone
 
 
class Conversation(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_conversations'
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        unique_together = ('student', 'tutor')
        ordering = ['-updated_at']
 
    def __str__(self):
        return f"{self.student.get_full_name()} ↔ {self.tutor.get_full_name()}"
 
    def get_other_user(self, user):
        return self.tutor if user == self.student else self.student
 
    def unread_count_for(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()
 
    def last_message(self):
        return self.messages.order_by('-created_at').first()
 
 
class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages'
    )
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='message_attachments/', null=True, blank=True)
 
    class Meta:
        ordering = ['created_at']
 
    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at:%H:%M}"
 
    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])


