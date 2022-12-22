from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField, ListField
from rest_framework import serializers

from accounts.models import Jobs
from accounts.serializers import AccountSerializer
from accounts.models import Account,UserProfile
from accounts.serializers import UserproflieSerializer
from accounts.serializers import UserEducationSerializer, UserExperienceSerializer
from accounts.models import CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields= '__all__'
        
class JobsSerializer(serializers.ModelSerializer):
    applicant=AccountSerializer(many=True)
    creater=AccountSerializer(read_only=True)
    Company=CompanyProfileSerializer(read_only=True)

    class Meta:
        model = Jobs
        fields= '__all__'
        

class JobdataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields= '__all__'
        
# class SkillSerializer(ModelSerializer):
#     class Meta:
#         model = Skill
#         fields= '__all__'

class cvSerializer(serializers.ModelSerializer):
    userprofile=UserproflieSerializer()
    userexperience=UserExperienceSerializer(many=True)
    usereducation=UserEducationSerializer(many=True)
    
    class Meta:
        model = Account
        fields= '__all__'

        