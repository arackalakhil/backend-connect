
from django.db import models

from accounts.models import Account

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import json

class Message(models.Model):
     sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')        
     receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')        
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read = models.BooleanField(default=False)
     thread_name=models.CharField(max_length=500,null=True,blank=True)
#    def save(self,*args,**kwars):
#             print("save called")
#             channel_layer=get_channel_layer()
#             message_obj=Message.objects.all()
#             data={}
#             super(Message,self).save(*args,**kwars)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)


class Notification(models.Model):
      notified_user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="notifieduser",null=True)
      notified_by=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="notifiedby",null=True)
      notification=models.TextField(max_length=100,null=True)
      thread_name=models.CharField(max_length=100,null=True)
      timestamp = models.DateTimeField(auto_now_add=True,null=True)
      is_seen=models.BooleanField(default=False)
      count=models.IntegerField(null=True,default=0)
      # def save(self,*args,**kwars):
      #       print("save                called")
      #       channel_layer=get_channel_layer()
      #       notification_obj=Notification.objects.filter(is_seen=False).count()
      #       print(notification_obj)
      #       data={"count":notification_obj,"current_notification":self.notification}
      #       async_to_sync (channel_layer.group_send)(
      #             "test_consumer_group",{
      #                   "type":"send_notification",
      #                   "value":json.dumps(data)
      #             }
      #       )
      #       super(Notification,self).save(*args,**kwars)


      def __str__(self):
           return str(self.notified_by)
    