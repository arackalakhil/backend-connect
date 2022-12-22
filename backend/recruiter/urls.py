
from django import views
from django.conf import settings
from rest_framework import routers
from django.urls import include, path
from django.conf.urls.static import static
from accounts.views import *
from recruiter.views import Comanyprofile
from recruiter.views import Applicantprofile
from recruiter.views import DeleteJob,JobData,Displayjob,DisplayAlljob

posts_router =routers.DefaultRouter()
posts_router.register("alljob", DisplayAlljob,basename="alljob"),
# router.register('ln/languages', views.LanguageView, basename='languages')
urlpatterns = [

    path('', JobData.as_view()),
    path("deletejob/<int:id>",DeleteJob.as_view()),
    path('', include(posts_router.urls)),
    # path("alljob",DisplayAlljob.as_view()),
    path('cvdata/<int:id>',Applicantprofile.as_view()),
    path("comanyprofile",Comanyprofile.as_view())





]