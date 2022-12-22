from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import  api_view
from channels.layers import get_channel_layer
from rest_framework.views import APIView
from asgiref.sync import async_to_sync
import json
import time
from rest_framework import permissions


from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from accounts.models import Account
from accounts.serializers import AccountSerializer
from accounts.serializers import UserproflieSerializer
from chat.serializer import Chatprofileserializers
from chat.models import Message
from chat.serializer import MessageSerializer
from django.db.models import Q
from rest_framework import viewsets
from pyChatGPT import ChatGPT
import openai
# Create your views here.

class Home(APIView):
    def get(self,request):
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        for i in range(1,10):
            channel_layer=get_channel_layer()
            data={'count':i}
            print(data)
            async_to_sync (channel_layer.group_send)(
                "test_consumer_group",{
                        "type":"send_notification",
                        "value":json.dumps(data)
                  }

            )
            time.sleep(1)
        data={"Asasasasas":"Asasasasasas"}
        print("1212121212121212121212121212121212121")


        return Response(data,status=status.HTTP_100_CONTINUE)
# ////////////////////////////////////////////////////


# Create your views here.


@api_view(['GET'])
def chatusers_list(request):
    print('req')
    print('ussss',request.user.username)
    # users = Account.objects.exclude(username = request.user.username)
    accounts = Account.objects.exclude(username=request.user.username)
    chat_list = set()
    print("accounttttttttttttttttt",accounts)
    print('555555555555555555555555555555555555',request.user)
    chat_users = Message.objects.filter(Q(sender=request.user.id) | Q(receiver=request.user.id))
    # print('99999999999999999999999999999999999999888888888',chat_users)
    
    for chat_user in chat_users:
        print('00000000..............',request.user)
        if str(request.user.id) in chat_user.thread_name:
            print('0000000000000000002222222222222222222222',request.user)
            print('hjhj',chat_user.receiver,'ll',chat_user.sender)
            chat_list.add(chat_user.sender)
            chat_list.add(chat_user.receiver)
            
    print('2222222222222222222555555555555555555',chat_list)
    
    user_list = []
    for user in accounts:
        print('121212121212121212121121',request.user)
        if user in chat_list:
            print('username',user)   
            user_list.append(user) 
    print(user_list)
    

    user_ser = Chatprofileserializers(user_list, many=True,context={'request':request})
    print("sera",user_ser.data)
    return Response(user_ser.data)


@api_view(['GET'])
def chat_data(request,username):
    user_obj = Account.objects.get(username=username)
    print('reciever',user_obj.id,'sender',request.user)
    users = Account.objects.exclude(username = request.user.username)
    if request.user.id > user_obj.id:
        thread_name = f'chat_{request.user.id}-{user_obj.id}'
    else:
        thread_name = f'chat_{user_obj.id}-{request.user.id}'  
    message_obj = Message.objects.filter(thread_name=thread_name)    
    chat_ser = MessageSerializer(message_obj,many=True)
    print(chat_ser.data)
    print('lll',user_obj.username,request.user.id)
    # print('message_obj',chat_ser.data) 
    return Response(chat_ser.data) 
    # return Response('data data')

class DisplayUserToChat(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    queryset=Account.objects.all()
    serializer_class=Chatprofileserializers
   

    def get_queryset(self):
        qsa = Account.objects.all().exclude(id=self.request.user.id).order_by('-id')
        username =self.request.query_params.get("username")
        if username is not None:
                    qs =qsa.filter(username__icontains=username)
                    print(qs)
                    if  qs:
                        print("000000000000000000000" , username )
                        return qs
                    qs = qsa.filter(first_name__icontains=username   ) |  qsa.filter(last_name__icontains=username   ) | qsa.filter(email__icontains=username   ) 
                    print(qs)
                    if qs is not None:
                        return qs


class Answer(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        user_message = request.data['question']
        print(user_message)
        print("Dddddddddddddddddddddddddddddddddddd")
        openai.api_key = "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"
        engine = "text-davinci-002"
        completion  = openai.Completion.create(engine=engine, prompt=user_message, max_tokens=1024, temperature=0.5)
        chatbot_response = completion.choices[0].text
        return JsonResponse({'response': chatbot_response})