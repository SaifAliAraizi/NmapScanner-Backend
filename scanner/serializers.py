from .models import Contact
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from .models import ScanRecord

class ScanRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanRecord
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message', 'send_copy']