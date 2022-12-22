
import re
from rest_framework import serializers

from chat.models import Notification
from . models import Account, Education, Experience, Jobs, UserProfile
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ListField
from rest_framework import serializers



class AccountSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style={'input':'password2'},write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Account
        expect="password"
        fields = ['id','first_name', 'last_name', 'username', 'email','phone_number', 'password', 'password2',"is_active","is_recruiter" ]
        # extra_kwargs = {'password': {'write_only': True}}
    def save(self,email_otp):
        register=Account(
          username=self.validated_data["username"],
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            phone_number=self.validated_data["phone_number"],
            email_otp=email_otp ,
            is_recruiter=self.validated_data["is_recruiter"],
            
            )
        password=self.validated_data["password"]
        print(password)
        password2=self.validated_data["password2"]
        print(password2)
        if password != password2:
            raise serializers.ValidationError({'password':'password dosent match'})
        print(password)
        print(type(password))
        
        register.set_password(password)
        register.save()
        return register

# class UserskillsSerializer(ModelSerializer):
#     # user=AccountSerializer(many=True)
#     # profile=UserproflieSerializer()
    
    
 
#     class Meta:
#         model = Skill
#         fields= ["skill"]


class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField()
    email_otp=serializers.CharField()




class UserproflieSerializer(ModelSerializer):
    # userprofile=AccountSerializer()
    class Meta:
        model = UserProfile
        fields=  '__all__'
        depth = 1


# class UserproflieSerializer(ModelSerializer):
    
    
#     class Meta:
#         model = Account
#         fields=  '__all__'
#         depth = 1

class UserProjectSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields= '__all__'


    


class UserEducationSerializer(ModelSerializer):
    
    user=AccountSerializer() 
    class Meta:
        model = Education
        fields= '__all__'
      


class UserExperienceSerializer(ModelSerializer):
    # user=AccountSerializer() 

    class Meta:
        model = Experience
        fields= '__all__'
    

class Passwordserializer(ModelSerializer):
    class Meta:
        model = Account
        fields= '[passsword,new_password]'

    def validate(self,data):
        # password=data["password"]
        new_password=data["new_password"]
        # password_patten=re.compile(r'^[a-zA-Z0-9]{8}[0-9][A-Za-z]$')
        # if password == new_password:
        return data
        # else :
        #        raise serializers.ValidationError({
        #         "false":"password not matched"
        #     })


class Notiicationserializer(ModelSerializer):
    # notified_by=AccountSerializer()
    # userprofile=UserproflieSerializer(source=AccountSerializer)
    class Meta:
        model = Notification
        fields= ["notified_user","notified_by","notification", "count","timestamp"]


# class Companyserializer(serializers.ModelSerializer):
#     password2= serializers.CharField(style={'input':'password2'},write_only=True)
#     class Meta:
#         model = Account
#         fields = ['id','company_name', 'email','phone_number','city','state','address', 'password', 'password2' ]
#         # extra_kwargs = {'password': {'write_only': True}}
#     def save(self):
#         register=Account(
#           username=self.validated_data["username"],
#             email=self.validated_data["email"],
#             first_name=self.validated_data["first_name"],
#             last_name=self.validated_data["last_name"],
#             phone_number=self.validated_data["phone_number"],
            
#             )
#         password=self.validated_data["password"]
#         print(password)
#         password2=self.validated_data["password2"]
#         print(password2)
#         if password != password2:
#             raise serializers.ValidationError({'password':'password dosent match'})
#         print(password)
#         print(type(password))
        
#         register.set_password(password)
#         register.save()
#         return register
