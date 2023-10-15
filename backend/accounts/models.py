from distutils.command.upload import upload
from email.mime import image
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from operator import mod
from django.db import models
# Create your models here.


# class Skill(models.Model):
#     skill = models.CharField(max_length=50)

#     def __str__(self):
#         return str(self.skill)


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an e-mail address')
        
        if not username:
            raise ValueError('User must have an Username')

        user = self.model(
            email       = self.normalize_email(email),
            username    = username,
            first_name  = first_name,
            last_name   = last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email      = self.normalize_email(email),
            username   = username,
            password   = password,
            first_name = first_name,
            last_name  = last_name
        )
        
        user.is_admin   = True
        user.is_active  = True
        user.is_staff   = True
        user.is_superadmin  = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50,null=True)
    email_otp       = models.IntegerField(null=True)
    reports         = models.IntegerField(null=True,default=0)
    #Required fields
    # image           = models.ImageField(upload_to='profile image',null=True)

    date_joined     = models.DateTimeField(auto_now_add=True)  
    last_login      = models.DateTimeField(auto_now_add=True)  
    is_verified     = models.BooleanField(default=False)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_recruiter    = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD      = 'username'
    REQUIRED_FIELDS     = ['email', 'first_name', 'last_name']

    objects = MyAccountManager()


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


# class Comapny(models.Model):
    
#     user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
#     fullname=models.CharField(max_length=50,null=True)
#     phone=models.IntegerField(null=True)
#     company_name=models.CharField(max_length=500,null=True)
#     city=models.CharField(max_length=50,null=True)
#     state=models.CharField(max_length=50,null=True)
#     email=models.CharField(max_length=50,null=True)
#     address=models.CharField(max_length=500,null=True)
#     image=models.ImageField(upload_to="images",null=True)
#     approved= models.BooleanField(default=False)
#     declined= models.BooleanField(default=False)
#     pending= models.BooleanField(default=True)
#     allotted= models.BooleanField(default=False)


#     class Meta:
#         verbose_name        = 'Booking'
#         verbose_name_plural = 'Booking'
        
#     def __str__(self):
#         return str(self.company_name)

class UserProfile(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE,related_name="userprofile",null=True)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    objective=models.CharField(max_length=500,null=True)
    # userskil = models.ManyToManyField(Skill, blank=True,related_name="userskill")
    skill = models.CharField(max_length=500,null=True)
    skil2 = models.CharField(max_length=500,null=True)
    skil3 = models.CharField(max_length=500,null=True)


    def __str__(self):
        return str(self.user)

class CompanyProfile(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE,related_name="companyprofile",null=True)
    company_name=models.CharField(max_length=500,null=True)
    vision=models.CharField(max_length=500,null=True)
    location=models.CharField(max_length=500,null=True)
    number=models.CharField(max_length=500,null=True)
    def __str__(self):
        return str(self.company_name)

class MyProjects(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="project",null=True)
    image=models.ImageField(upload_to="images",null=True)
    projectname=models.CharField(max_length=50,null=True)
    projectdetails=models.CharField(max_length=500,null=True)
    
    def __str__(self):
        return str(self.user)
    
class Experience(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="userexperience",null=True)
    company=models.CharField(max_length=500,null=True)
    Post=models.CharField(max_length=500,null=True)
    join_date=models.DateTimeField(null=True)
    Leave_date=models.DateTimeField(null=True)
    aim=models.CharField(max_length=500,null=True)
    
    def __str__(self):
        return str(self.user)

class Education(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,related_name="usereducation",null=True)
    institution=models.CharField(max_length=500,null=True)
    type=models.CharField(max_length=500,null=True)
    join_date=models.DateTimeField(max_length=50,null=True)
    Leave_date=models.DateTimeField(null=True)

    aim=models.CharField(max_length=500,null=True) 
    
    def __str__(self):
        return str(self.user)




# class Ceategory(models.model):
#     """Men"""
#     """Women"""
#     cat = models.CharField(max_length=50)
# class Product(models.Model):
#     """Many to One Relationship"""
#     cat = models.ForeignKey(Ceategory, on_delete=models.CASCADE, related_name='products')
#     name = models.CharField(max_length=50)
# """
#  cat = Category.objects.get(id=1)
#     prod = cat.product_set.all()
#     print(prod)
#   """



class Jobs(models.Model):
    STATUS =(('Full time','Full time'),
                ("Part time","Part time"),
                ("Internship","Internship  "),
                )
    creater = models.ForeignKey(Account,on_delete=models.CASCADE, blank=True,related_name="jobcreater")
    heading = models.CharField(max_length=500,null=True)
    description = models.CharField(max_length=500,null=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True)
    applied_on= models.DateTimeField(auto_now=True)  
    Company=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE, default=None, blank=True,related_name="company")
    type = models.CharField(max_length=100,choices=STATUS,default="order conformed",null=True)
    applicant= models.ManyToManyField(Account, blank=True,related_name="jobseeker")
    # jobskill = models.ManyToManyField(Skill,blank=True,related_name="Jobskill")
    skill = models.CharField(max_length=500,null=True)
    skil2 = models.CharField(max_length=500,null=True)
    skil3 = models.CharField(max_length=500,null=True)
    number_of_appicants =models.IntegerField(null=True,default=0)
    number_of_reports=models.IntegerField(null=True,default=0)
    is_active = models.BooleanField(default=True)



    def __str__(self):
        return str(self.heading)
    


