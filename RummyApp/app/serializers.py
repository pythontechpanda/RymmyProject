from rest_framework import serializers
from .models import *
from django.contrib import auth

class RegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'password', 'profile_picture', 'first_name', 'middle_name', 'last_name', 'email','city', 'state', 'pincode', 'gender','date_of_birth','mobile_no','is_verified', 'is_above18', 'is_user','device_registration_id']
    def validate(self, attrs):
        username = attrs.get('username', '')
        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
    
    
    