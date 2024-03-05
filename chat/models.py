from django.db import models

# Create your models here.

class Chatroom(models.Model):
    roomname = models.CharField(max_length=40, default='noname')
    detail = models.CharField(max_length=80, default='nothing')
    mainuser = models.IntegerField()

class Chathistory(models.Model):
    chatroomid = models.IntegerField()
    history = models.CharField(max_length=20000)

class Groupnumber(models.Model):
    roomid = models.IntegerField()
    groupuserid = models.IntegerField()