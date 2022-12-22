
from django import views
from django.conf import settings
from rest_framework import routers
from django.urls import include, path
from django.conf.urls.static import static
from accounts.views import *
from . import views
posts_router =routers.DefaultRouter()

posts_router.register("displayusertochat", views.DisplayUserToChat,basename="displayusertochat"),

urlpatterns = [
    path('', views.Home.as_view()),
path('chat-list',views.chatusers_list,name='chat_list'),
    path('chat-data/<str:username>',views.chat_data,name='chat_data'),
    path("answer",views.Answer.as_view()),
    # path("data",views.DisplayUserToChat.as_view()),
    path('', include(posts_router.urls)),

    
]