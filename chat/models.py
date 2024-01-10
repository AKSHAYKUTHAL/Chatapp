from django.db import models
from django.contrib.auth.models import User



class Message(models.Model):
    author = models.ForeignKey(User,on_delete = models.CASCADE, related_name="author_message" )
    receiver  = models.ForeignKey(User,on_delete = models.CASCADE, related_name="receiver_message" ,blank=True, null=True)
    content = models.TextField()
    room_name = models.CharField(max_length=25,blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.username
    