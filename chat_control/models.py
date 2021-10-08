from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Threads(models.Model):
    me = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_thread")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_thread")
    private_channel_name = models.CharField(null=True, max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.private_channel_name:
            self.private_channel_name = f"{self.me.username}-{self.recipient.username}"

        return super(Threads, self).save(*args, **kwargs)

    @property
    def private_name(self):
        if self.private_channel_name:
            return self.private_channel_name
        else:
            return "Error"

    class Meta:
        verbose_name_plural = "Threads"


class Message(models.Model):
    thread = models.ForeignKey(Threads, on_delete=models.CASCADE,
                               related_name="messages_for_thread", null=True)
    sender = models.ForeignKey(User, null=True, on_delete=models.PROTECT,
                               related_name="my_messages")
    recipient = models.ForeignKey(User, null=True, on_delete=models.PROTECT,
                                  related_name="recipient_message")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} sent {self.recipient.username} a message"

    @property
    def last_5_messages(self):
        return Message.objects.order_by('-created').all()[:5]

    class Meta:
        ordering = ('-created', )
