from email import utils
import random
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from accounts.serializers import *
from accounts.email import send_otp_email
from django.core.mail import send_mail
from rest_framework import permissions
from django.core import serializers
from recruiter.serializers import CompanyProfileSerializer
from recruiter.serializers import cvSerializer
from recruiter.serializers import JobsSerializer,JobdataSerializer
import json
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import viewsets




class JobData(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post (self,request):
    
            
            data={}
            print("qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq")
            user=request.user
            print(request.data)
            serializer=JobdataSerializer(data=request.data)
            print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            if serializer.is_valid():
        

                print("9999999999999999999999999999999999999999999999999999999")
                serializer.save()

                return Response(serializer.data,status=status.HTTP_201_CREATED )
            else:
                print(serializer.errors)
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND )

        
                print(serializer.errors)
                data["e"]='errrorrrr'
                print("ddddddddddddddddddddddddddddddddddddddddddd")

                return Response(data,status=status.HTTP_404_NOT_FOUND)
    def get (self,request):
        serializer=None
        try:
            user =request.user.id
            print('ddddd',request.user)
            print(user)
            print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            user_jobs= Jobs.objects.filter(creater=user)
            print(user_jobs)
            serializer = JobsSerializer(user_jobs,many=True)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except: 
            return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
    def put (self,request):
        print('reqqqq',request.data)
        job_id = request.data['id']
        jobs = Jobs.objects.get(id=job_id)
        serializer=JobdataSerializer(jobs, data=request.data)

        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
   






class DeleteJob(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self,request,id):
        try:
            user =request.user
            education=Jobs.objects.get(id=id,creater=user)
            education.delete()
            
            return Response (status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

# class Reportjob(APIView):
#     permission_classes=[permissions.IsAuthenticated]
#     def put(sel)


# //////////////////////////////////////////////////////User Job side/////////////////////////////////////
class DisplayAlljob(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset=Jobs.objects.all()
    serializer_class=JobsSerializer
   
    
    def get_queryset(self):
        qsa = Jobs.objects.all().order_by('-id')

        heading =self.request.query_params.get("heading")
        print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj",heading)
        # skills=self.request.query_params.get("heading")
        if heading is not None:
            qs =qsa.filter(heading__icontains=heading)
            print(qs)
            if  qs:
                print("000000000000000000000")
                return qs
            print(qs)
            print("fffffffffffffffffffffffffffffff",heading)
            qs = qsa.filter(skill__icontains=heading   ) |  qsa.filter(skil2__icontains=heading   ) | qsa.filter(skil3__icontains=heading   ) 
            print(qs)
            if qs is not None:
                return qs

        # if skills  is not None:
            # qs = qs.filter(skil2__icontains=skills)
        return qs





class Displayjob(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self,data):
        try:
            return Jobs.objects.filter(skills=data["skil1"]) or Jobs.objects.filter(skills=data["skil2"]) or Jobs.objects.filter(skills=data["skil3"])
        except:
            pass

    def get(self,request):
        serializer=None
        try:
            user=request.user
            data=request.data
            print("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
            print(user)
            userprofile=UserProfile.objects.get(user=user)
            print(userprofile.skill)
            print("Dddddddddddddddddddddddddddddddddddddddddddd")
            
        except:
            pass


# ///////////////////Applicant profile//////////////////

class Applicantprofile(APIView):
        # permission_classes = [permissions.IsAuthenticated]

        def get(self,request,id):
            print(id)
            print("idididididididiidididididiididididididiidididididid")
            user=Account.objects.get(id=id)
            print(user)
            
            serializer=cvSerializer(user,context={'request':request})
            print(serializer)
            return Response(serializer.data,status=status.HTTP_200_OK)


# /////////////////////////////////////company Profile///////////////////////
class Comanyprofile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        serializer=None
        try:
            user=request.user
            if Account.objects.get(username=user):
                recruiter=Account.objects.get(username=user)
                Companydata=CompanyProfile.objects.get(user=recruiter)
                serializer = CompanyProfileSerializer(Companydata,context={'request':request})
                return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        print("rrrrrrrrrrrrr",request.data)
        print(request.data)
        serializer=CompanyProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)
        