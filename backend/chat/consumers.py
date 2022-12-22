import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import Account
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from chat.models import Notification,Message

class ChatConsumer(WebsocketConsumer):
    def connect(self):  
        self.room_name = "test_consumer"
        self.room_group_name="test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
           self.room_group_name,  self.channel_name,
        )
        self.accept()
        self.send(text_data=json.dumps({'status':"connected to django channels"}))
    def receive(self,  text_data):
        print(text_data)
        self.send(text_data=json.dumps({"status":"we got your data"}))

      
    def disconnect(self, *args,**kwargs):
        print(" disconnected from socket")
        

    def send_notification(self, event):
        print("send notification")
        data=json.loads(event.get("value"))
    
        # self.send(text_data=json.dumps({"payload":data}))
        self.send(text_data=json.dumps({"payload":data}))

# /////////////////////notifications//////////////////////////
class NewConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
      
      
        other_user_id = self.scope['url_route']['kwargs']['id']
        print('other id',other_user_id)

        # if int(my_id) > int(other_user_id):
        #     self.room_name = f'{my_id}-{other_user_id}'
        # else:
        self.room_name = f'{other_user_id}'  

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )   
        await self.accept()
    # async def connect(self):
    #     self.room_name='new_consumer'
    #     self.room_group_name="new_consumer_group"
    #     await(self.channel_layer.group_add)(
    #        self.room_group_name,  
    #        self.channel_name
    #     )
    #     await self.accept()
    #     await self.send(text_data=json.dumps({"status":"connected to new async jsonconsumers"}))
    
    async def receive(self,  text_data):
        data = json.loads(text_data)
        print("datasssssssssssssssssssssssssssssss",data)
        notified_user= data['notified_user']
        notified_by = data["notified_by"]
        notification=data["notification"]
        # await self.save_notification(notified_user,notified_by,notification,self.room_group_name)
        
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #           {
        #                 "type":"send_notification",
        #                 "value":text_data
        #           }
        #     )
        # await self.send_notification("notifys")


    async def disconnect(self, *args,**kwargs):
        print(" disconnected from socket2") 
  
    async def send_notification(self, event):
        print("send notificationssssssssssssssssss")
        data=json.loads(event.get("value"))
        print(data)
        print("55555555555555555555555555555555555555555555555")
        await self.send(text_data=json.dumps({"payload":data}))




    @database_sync_to_async
    def save_notification(self,notified_user,notified_by,notification,thread_name):
        Notification.objects.create(notified_user=Account.objects.get(id=notified_user),notified_by=Account.objects.get(id=notified_by),notification=notification,thread_name=thread_name)
# ///////////////////////////////////////////////////////////////////////
class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # my_id = self.scope['user'].id
        my_id = self.scope['url_route']['kwargs']['myid']
        # my_id=3
        print('my id',my_id)
        other_user_id = self.scope['url_route']['kwargs']['id']
        print('other id',other_user_id)

        if int(my_id) > int(other_user_id):
            print('my printid',my_id)
            self.room_name = f'{my_id}-{other_user_id}'
        else:
            print('otherkkkk id',other_user_id)
            self.room_name = f'{other_user_id}-{my_id}'    

        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )   

        await self.accept() 
        # await self.send(text_data=self.room_group_name)

    async def disconnect(self,code):
        print('sajdkfh')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self,text_data=None,bytes_data=None):
        data = json.loads(text_data)
        messsage = data['message']
        username = data['username']
        reciever_user = data['reciever_user']

        await self.save_messages(username,self.room_group_name,messsage,reciever_user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':messsage,
                'username':username,
                'reciever_user':reciever_user
            }
        )

    async def chat_message(self,event):
        message = event['message']
        username = event['username'] 
        reciever_user = event['reciever_user']  

        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'reciever_user':reciever_user
        }))  

    @database_sync_to_async
    def save_messages(self,username,thread_name,message,reciever_user):
        sender = Account.objects.get(username=username)
        reciever = Account.objects.get(username=reciever_user)
        Message.objects.create(
            sender=sender,receiver=reciever,thread_name=thread_name,message=message
        )