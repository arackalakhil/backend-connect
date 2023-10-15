
from django.conf import settings
from django.urls import include, path
from accounts.views import *
from rest_framework import routers

from . views import  RegisterUser, VerifyOTP


urlpatterns = [
    path("learn",learn.as_view()),
    path('register', RegisterUser.as_view()),
    path('verifyotp',VerifyOTP.as_view()),

    path('education',UserEducation.as_view()),
    path('experience',UserExperience.as_view() ),


    path('data',UserData.as_view() ),



    
    path('userprofile', ViewUserProfile.as_view() ),
    path('getuserskill', UserSkill.as_view() ),
    


    path('deleteEducation/<int:id>', deleteEducation.as_view() ),
    path('deleteExperience/<int:id>', deleteExperience.as_view() ),





    path("editeducation",EditEducation.as_view()),
    path("applyjob",Applyjob.as_view()),
    path("withdrawjob",Withdrawjob.as_view()),
    path("reportjob",Reportjob.as_view()),

    path("forgotpassword",ForgotPassword.as_view()),
    path("changepassword",ChangePassword.as_view()),


    path("test",Test.as_view()),
    path("notifications",NotificationUser.as_view()),







]