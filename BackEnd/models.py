from django.db import models


# Create your models here.
class ChatRooms(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(default="", max_length=20)


class Messages(models.Model):
    id = models.AutoField(primary_key=True)
    chatroom = models.ForeignKey('ChatRooms', on_delete=models.CASCADE)
    user_id = models.IntegerField()
    name = models.CharField(default="", max_length=20)
    message = models.CharField(default="", max_length=200)
    message_time = models.DateTimeField(auto_now_add=True)

class Tokens(models.Model):
    id=models.AutoField(primary_key=True)
    user_id=models.IntegerField(null=False)
    token=models.CharField(null=False,max_length=256)

