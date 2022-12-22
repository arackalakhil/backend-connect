from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import AccountSerializer,VerifyAccountSerializer
from accounts.models import Account
# Create your views here.
import jwt

from accounts.models import UserProfile

class UserData(APIView):
    def get(self,request):
        account=Account.objects.all()
        list=AccountSerializer(account,many=True)
        if list:
            print(list.data)
            return Response(list.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)




class Usermanipulation(APIView):
    def post(self,request,id):
        token = request.GET.get('token')
        try:
            account=Account.objects.get(id=id)
            if account.is_active == True:
                account.is_active=False
                account.save()
            else:
                account.is_active = True
                account.save()

            print(account)
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
    
    def delete(self,request,id):
        try:
            account=Account.objects.get(id=id)
            account.delete()
            return Response (status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    