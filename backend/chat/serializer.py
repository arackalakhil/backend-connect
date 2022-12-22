
from rest_framework import serializers
from accounts.models import Account
from accounts.serializers import UserproflieSerializer

from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    # sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Account.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=Account.objects.all())
    # # sender=
    class Meta:
        model = Message
        # fields = ['sender', 'receiver', 'message', 'timestamp']
        fields = '__all__'

class Chatprofileserializers(serializers.ModelSerializer):
    userprofile=UserproflieSerializer()
    class Meta:
        model = Account
        fields = '__all__'
