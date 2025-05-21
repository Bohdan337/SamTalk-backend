from django.db import models
from user.models import CustomUser
import shortuuid


# Create your models here.
class Chat(models.Model):
    members = models.ManyToManyField(CustomUser, related_name='members', blank=True)
    is_admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='is_admin', null=True, blank=True)
    online_members = models.ManyToManyField(CustomUser, related_name='online_members', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='author')
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.author.username} : {self.content}"