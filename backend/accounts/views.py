from email import utils
import random
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import AccountSerializer,VerifyAccountSerializer
from accounts.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from accounts.serializers import *
from accounts.email import send_otp_email
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework import viewsets
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from rest_framework.parsers import MultiPartParser, FormParser
from recruiter.serializers import JobsSerializer

# from accounts.serializers import Companyserializer
from django.http import JsonResponse
# from  .utils import Utilsx
# Create your views here.
class learn(APIView): 
    def get(self,request):
        data={"message": "i am good"}
        return JsonResponse(data)
class RegisterUser(APIView):
    def post(self, request):
        user=request.data
        
        print(request.data)
        userserializer=AccountSerializer(data=request.data)
        datas={} #to pass data to front end just for verification not nessery
        if userserializer.is_valid():
            print("222222222222222222222222222222222222222222222222222222222222222")
            print(userserializer)
            print("222222222222222222222222222222222222222222222222222222222222222")
            subject='your account verification email '
            email_otp=random.randint(1000,9999)
            message= f"your otp is {email_otp}"
            email_from=settings.EMAIL_HOST
            accounts=userserializer.save(email_otp)
            print(userserializer.data['email'])
            print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
            try:
                send_mail(subject,message,email_from,[userserializer.data['email']])
                
                print("Ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
                return Response(status=status.HTTP_202_ACCEPTED)
            except:
                print("ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
                pass
            # user_obj=Account.objects.get(email=email)
            # user_obj.email_otp=otp
            # user_obj.save()
            # # send_otp_email(userserializer.data["email"])

 
           
            # user_data =userserializer.data
            # # token=RefreshToken.for_user(user)
            # # current_site=get_current_site(request
            # # data={"domain".current_site.delete}
            # # Util.send_email(data)



            # datas['username']=accounts.username #to pass data to front end just for verification not nessery
            # datas['responce']='Account registered'#to pass data to front end just for verification not nessery
            # return Response( status=status.HTTP_201_CREATED)
        else:
            print("errors",userserializer.errors)
            return  Response(
                {
                    'data':userserializer.errors,
                    'message':"some thing went wrong"

                },status=status.HTTP_400_BAD_REQUEST
            )

class VerifyOTP(APIView):
    def post(self,request):
        try:
            print(request.data)
            serializer=VerifyAccountSerializer(data=request.data)
            if serializer.is_valid():
                email_id=serializer.data["email"]
                otp=int(serializer.data["email_otp"])

                print(type(otp))
                try:
                    try:
                        user=Account.objects.get(email=email_id)
                        print(user)
                        if(user.email_otp == otp):
                            print("ggggggggggggggggggggggggggggggggggggggggggggggggggg")
                            if user.is_active==False:
                                user.is_active=True
                                user.save()
                                return Response(status=status.HTTP_201_CREATED)

                            else :
                                print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
                                return  Response(
                                {
                                'message':"account already active"
                                },status=status.HTTP_400_BAD_REQUEST
                            )
                        else:
                            print("llllllllllllllllllllllllllllllllllllll")
                            return Response(status=status.HTTP_204_NO_CONTENT)
                            return  Response(
                                {
                                'message':"Otp dont match"
                                },status=status.HTTP_100_CONTINUE
                            )
                    except:
                        return  Response(
                                {
                                'message':"no account found please create one"
                                },status=status.HTTP_400_BAD_REQUEST
                            )


                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            print("////////////////////////////////////////////////////////////////////////////")

# class RegisterCompnay:
#     def post (self,request):
#         company=request.data
#         companyserializer=Companyserializer(data=request.data)
# //////////////////////////////////////add details///////////////////////////////////////////////////////////



# def post(self,request):
#         print(request.data)
#         booking=NewBookingserializer(data=request.data)
#         print("Aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
#         if booking.is_valid():
#             booking.save()
#             return Response(status=200)
#         else:
#             data=booking.errors
#             return Response(status=status.HTTP_404_NOT_FOUND)
# //////////////////////////////account details///////////////////////
class UserData(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request):

        serializer=None
        try:
            # user =request.user.id
            print("fffffffffffffffffffffffffffffffffffffffffff")
            user_qualifiactions= Account.objects.filter(username="amal")
            print(user_qualifiactions)
            print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnoooooooooooooooooo")
            serializer = AccountSerializer(user_qualifiactions)
            print("sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
            print(serializer)
            return Response(serializer, status=status.HTTP_200_OK)
        except:
            print("ooooooooooooooookkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
            
# /////////////////////EDUCATION///////////////////////////////////////////////////////////////////////////////////////////////////

class UserEducation(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):

        serializer=None
        try:
            user =request.user.id
            print('ddddd',request.user)
            print(user)
            user_qualifiactions= Education.objects.filter(user=user)
            print(user_qualifiactions)
            serializer = UserEducationSerializer(user_qualifiactions,many=True)
            print(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except: 
            return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

    def post (self,request):
        try:
            user=request.user
            data={}
            print({user:request.user} ) 
            print('sdjkhf',request.data)
            #user= Account.objects.get(id=request.user.id)
            #educatiom = Education.objects.create(user=request.user,school=data["scho"])
            serializer=UserEducationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # data['resp']=serializer.data  
                print(serializer.data )
                return Response(data,status=status.HTTP_201_CREATED )
            else:
                data['err']=serializer.errors
                print(serializer.errors)
                return Response(data,status=status.HTTP_404_NOT_FOUND)
        except:
                data["e"]='errrorrrr'
                return Response(data,status=status.HTTP_404_NOT_FOUND)

    def put (self,request):
        print('reqqqq',request.data)
        edu_id = request.data['id']
        eduuu = Education.objects.get(id=edu_id)
        # education_data=self.get_objiect(id)
        serializer=UserEducationSerializer(eduuu, data=request.data)

        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)

class deleteEducation(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,id):
        try:
            user =request.user
            education=Education.objects.get(id=id,user=user)
            education.delete()
            
            return Response (status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

# ////////////////////////////////////////////////Experience///////////////////////////////////////////////////////


class UserExperience(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer=None
        try:
            user =request.user
            print(user)
            user_experience= Experience.objects.filter(user=user)
            print(user_experience)
            serializer = UserExperienceSerializer(user_experience,many=True)
            print(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except: 
            return Response(serializer.data,status=status.HTTP_404_NOT_FOUND)

    def post (self,request):
        try:
            user=request.user
            data={}
            print(user)
            print('sdjkhf',request)
            serializer=UserExperienceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data['resp']=serializer.data  
                return Response(data,status=status.HTTP_201_CREATED )
            else:
                data['err']=serializer.errors
                return Response(data,status=status.HTTP_404_NOT_FOUND)
        except:
                data["e"]='errrorrrr'
                return Response(data,status=status.HTTP_404_NOT_FOUND)

    def put (self,request):
        print('reqqqq',request.data)
        experience_id = request.data['id']
        experience = Experience.objects.get(id=experience_id)
        # education_data=self.get_objiect(id)
        serializer=UserExperienceSerializer(experience, data=request.data)

        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)

class deleteExperience(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request,id):
        try:
            user =request.user
            education=Experience.objects.get(id=id,user=user)
            education.delete()
          
            return Response (status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


            
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    












# ///////////////////////////////////////////////////////////////////////////////////////////////////////////

class ViewUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def get(self, request):
        serializer=None
        try:
            user=request.user
            data ={}
            if Account.objects.get(username=user):
                users=Account.objects.get(username=user)
        
                user_profile = UserProfile.objects.get(user=users)
                serializer = UserproflieSerializer(user_profile,context={'request':request})
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                data["err"]="create a profile"
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)

    def patch (self,request):
        serializer=None
        # try:
        print("datadatadadtaadadadadasdadadssddddddddddddddddddddddd",request.data)
        
        user=request.user
        
        data=request.data
        print(user)
        user_profile = UserProfile.objects.get(user=user)
        print("::::::::::::::",user_profile)
        user_profile.image=data.get("image",user_profile.image)
        user_profile.objective=data.get("objective",user_profile.objective)
        user_profile.skill=data.get("skill",user_profile.skill)
        user_profile.skil2=data.get("skil2",user_profile.skil2)
        user_profile.skil3=data.get("skil3",user_profile.skil3)
        user_profile.save()
        serializer=UserproflieSerializer(data=user_profile,context={"request":request})
       
        if serializer.is_valid():
         return Response(serializer.data,status=status.HTTP_201_CREATED)
    # except:
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post (self,request):
        print('user is',request.user.id)
        # print('skilll',request.data['skill'])
        # print('reqqqq',request.data)

        # edu_id = request.data['id']
        # eduuu = UserProfile.objects.get(id=edu_id)
        # education_data=self.get_objiect(id)
    
        serializer=UserproflieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            print("lllllllllllllllllllllllllllllllllllllll")
            return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)













class UserSkill(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        serializer=None
        try:
            user=request.user
            UserData=Account.objects.get(username=user)

            userskills=UserData.userskill.filter().values('skill')
            print(userskills)

            return Response(userskills, status=status.HTTP_200_OK)
        except:
            return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
    def post (self,request):
        try:
            user=request.user
            UserData=Account.objects.get(username=user)
            userskills=UserData.userskill.add()
        except:
            pass









class ViewUserskills(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        serializer=None
        try:
            user=request.user
            # userskils=Skill.objects.filter(user=user)
            # serializer =UserskillsSerializer(userskils,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(serializer.data, status=status.HTTP_200_OK)
            




# //////////////////////////////////DELETE//////////////////////////////////////////////












# ////////////////////////////////Edit//////////////////////////////////////////////////////////////////

class EditEducation(APIView):
        permission_classes = [permissions.IsAuthenticated]
    
        def put (self,request):
            print('reqqqq',request.data)
            edu_id = request.data['id']
            eduuu = Education.objects.get(id=edu_id)
            # education_data=self.get_objiect(id)
            serializer=UserEducationSerializer(eduuu, data=request.data)

            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_304_NOT_MODIFIED)








# //////////////////////////////////////////////////////////////////////
# class Userjobs(APIView):
#     permission_classes=[permissions.IsAuthenticated]
#     def get(self,request):
#         try:
#             return Jobs.objects.filter(skills=data["skil1"]) or Jobs.objects.filter(skills=data["skil2"]) or Jobs.objects.filter(skills=data["skil3"])
#         except:
#             pass











# ////////////////////////////////////////////////////////////////////////////////////////////////////
class Test(APIView):
    def get(self,request):
        channel_layer=get_channel_layer()

        notify=Notification.objects.filter(notified_user=3,is_seen=False)
        serializer = Notiicationserializer(notify,many=True)
       
        print("fffffffffffffffffffffff")
        async_to_sync (channel_layer.group_send)(
                    "test_consumer_group",{
                            "type":"send_notification",
                            "value":json.dumps(serializer.data)
                    }
                )
        print("---------------------",notify)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserDatas(APIView):

    def get(self,request,id):
    
        user=Account.objects.get(id=id)
        if request.data.get("first_name") == "" or request.data.get("last_name") == "":
            raise serializers.ValidationError({"error":"Fields cannot be blank"})
        user.first_name = request.data.get("first_name",)

        user.save()

# ////////////////////////////applyjob//////////////////////////


class Applyjob(APIView):

    permission_classes = [permissions.IsAuthenticated]


    def put (self,request):
        # try:
            print("/////////////////////////////////////////////////////////////")
            channel_layer=get_channel_layer()
            data={}
            print(request.data)
            creator_id=request.data['creator']
            user=request.user
            print(user.id )
            job_id = request.data['id']
            print(job_id)
           
            job=Jobs.objects.get(id=job_id)
            print(job)
            if user in job.applicant.all():
                data['error']="all ready applied"
                return Response(data,status=status.HTTP_208_ALREADY_REPORTED)
            job.applicant.add(user)
            job.number_of_appicants=1+job.number_of_appicants

            job.save()
            room_group_name = 'chat_%s' % f'{creator_id}'
            notify=Notification.objects.create(notified_user=Account.objects.get(id=request.data['creator']))
            notify.thread_name=room_group_name
            notify.notification=user.username+" applied for "+job.heading
            count_no=Notification.objects.filter(notified_user=Account.objects.get(id=request.data['creator']),is_seen=False).count()
            print(count_no)
            print("999999999999999999999999999999999999999999989898989")
            notify.count=count_no
            notify.notified_by=Account.objects.get(id=request.user.id)

            notify.save()
            print("dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
            notifications=Notification.objects.filter(is_seen=False,notified_user=Account.objects.get(id=request.data['creator'])).order_by("-id")[:1]
            count=Notification.objects.filter(is_seen=False,notified_user=Account.objects.get(id=request.data['creator'])).count()

            serializers=Notiicationserializer(data=notifications,many=True)
            print(room_group_name,"fffffffffffff")
            print(notifications,"vvvvvvvvvvvvvvvvvvvv")
            if serializers.is_valid():
                pass
            print("666666666666666666666666666666666666666666666",serializers.data)
            async_to_sync (channel_layer.group_send)(
                room_group_name,{
                    "type":"send_notification",
                    "value":json.dumps(serializers.data)
                }
        )
            print(serializers.errors)

            print("33333333333333333",notify)
            return Response(status=status.HTTP_201_CREATED)

        # except:

        #     return Response(status=status.HTTP_404_NOT_FOUND)
            
class Withdrawjob(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def put (self,request):
        try:
            print(request.data)

            user=request.user
            print(user.id )
            job_id = request.data['id']
            print(job_id)

            job=Jobs.objects.get(id=job_id)
            print(job)
            job.number_of_appicants-=1
            job.applicant.remove(user)
            job.number_of_appicants+=1
            job.save()
            return Response(status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
 
class Reportjob(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def put(self,request):
        try:
            print(request.data)

            user=request.user
            print(user.id )
            job_id = request.data['id']
            print(job_id)

            job=Jobs.objects.get(id=job_id)
            print(job)
            job.number_of_appicants-=1
            job.applicant.remove(user)
            job.number_of_appicants+=1
            job.save()
            return Response(status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

# ///////////////////forgot password/////////////////////////////////
class ForgotPassword(APIView):
    def put(self,request):
        try:
            if Account.objects.get(email=request.data["email"]):
                account=Account.objects.get(email=request.data["email"])
                subject='your account verification email '
                email_otp=random.randint(1000,9999)
                message= f"password reset  otp is {email_otp}"
                email_from=settings.EMAIL_HOST

                print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                try:
                    send_mail(subject,message,email_from,[request.data['email']])
                    account.email_otp=email_otp
                    account.save()
                    print("Ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
                    return Response(status=status.HTTP_202_ACCEPTED)
                except:
                    print("ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc")
                    pass
            else:
                   return  Response(
                                {
                                'message':"No email-matching account found"
                                },status=status.HTTP_200_OK
                            )
        except:
            pass
    def patch(self,request):
            account=Account.objects.get(email=request.data["email"])
            if account.email_otp==request.data["otp"]:
                return  Response(
                                {
                                'message':"otp matched"
                                },status=status.HTTP_200_OK
                            )

            else:
                return  Response(
                                {
                                'message':"wrong otp "
                                },status=status.HTTP_400_BAD_REQUEST
                            )
                
class ChangePassword(APIView):
    def put(self,request):
        try:
            serializers=Passwordserializer(data=request.data)
            account=Account.objects.get(email=request.data["email"])
            if serializers.is_valid():
                account.set_password(serializers.data.get('new_password'))
                account.save()
                return  Response(
                        {
                        'message':"password updated "
                        },status=status.HTTP_200_OK
                    )

        except:
            pass

    


# ///////////////////////////////////////////////////Notification////////////////////////////////////////////////////////////////
class NotificationUser(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        user=request.user
        channel_layer=get_channel_layer()
        notify=Notification.objects.filter(notified_user=Account.objects.get(id=user.id),is_seen=False).order_by("-id")
        print((notify))
        print(notify)
        serializer = Notiicationserializer(data=notify,many=True) 
        room_group_name = 'chat_%s' % f'{user.id}'
        print("9999999999999999999999")
        print(room_group_name)
        if serializer.is_valid():
            print("fffffffffffffffffffffff")
            async_to_sync (channel_layer.group_send)(
         
                        "room_group_name",{
                                "type":"send_notification",
                                "value":json.dumps(serializer.data )
                        }
                    )
        print("---------------------",notify)
        print("---------------------",serializer.errors)


        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request):
        user= request.user
        channel_layer=get_channel_layer()
        notify=Notification.objects.get(id=request.id,notified_user=Account.objects.get(id=user.id))
        notify.is_seen=True
        notify.save()
        notifs=Notification.objects.filter(notified_user=Account.objects.get(id=user.id),is_seen=False).last()
        notifs=notifs-1
        print(notify)
        notify_send=Notification.objects.filter(notified_user=Account.objects.get(id=user.id),is_seen=False).order_by("-id")
        print((notify))
        print(notify)
        serializer = Notiicationserializer(data=notify_send,many=True) 
        if serializer.is_valid():
            print("fffffffffffffffffffffff")
            async_to_sync (channel_layer.group_send)(
         
                        "room_group_name",{
                                "type":"send_notification",
                                "value":json.dumps(serializer.data )
                        }
                    )
        print("---------------------",notify)
        print("---------------------",serializer.errors)


        return Response(serializer.data,status=status.HTTP_200_OK)