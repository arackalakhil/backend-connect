
from django.contrib import admin
from django.urls import path , include
import debug_toolbar
from django.conf.urls.static import static

from backend import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.api.urls')),
    path('accounts/',include('accounts.urls')),
    path('admins/', include('admins.urls')),
    path('recruiter/', include('recruiter.urls')),
    path('recruiter/', include('recruiter.urls')),
    path('chat/', include('chat.urls')),




    path("__debug__/",include(debug_toolbar.urls)),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
