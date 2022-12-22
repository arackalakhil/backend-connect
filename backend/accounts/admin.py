from django.contrib import admin

from accounts.models import Account
from accounts.models import Education, Experience, UserProfile,MyProjects,Jobs
from accounts.models import CompanyProfile

# Register your models here.
admin.site.register(Account)
admin.site.register(UserProfile)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(MyProjects)
admin.site.register(CompanyProfile)
admin.site.register(Jobs)




