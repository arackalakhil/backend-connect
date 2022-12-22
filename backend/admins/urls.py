from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views



urlpatterns=[
    path('userdata',views.UserData.as_view()),
    path('usermanipulation/<int:id>',views.Usermanipulation.as_view()),
]+static(settings.MEDIA_URL,documnet_root=settings.MEDIA_ROOT)
