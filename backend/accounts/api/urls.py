from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




