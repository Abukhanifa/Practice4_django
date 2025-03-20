from rest_framework import serializers
from rest_framework.serializers import CharField
from .models import Item
from django.contrib.auth import get_user_model 
from rest_framework.validators import UniqueValidator 
from django.contrib.auth.password_validation import validate_password 

class ItemSerializer(serializers.ModelSerializer):
     class Meta:
        model = Item
        fields = '__all__'
        
        
User = get_user_model() 

 

class RegisterSerializer(serializers.ModelSerializer): 
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())]) 
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password]) 
    password2 = serializers.CharField(write_only=True, required=True) 

    class Meta: 
        model = User 
        fields = ('username', 'email', 'password', 'password2', 'role') 

    def validate(self, attrs): 
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({"password": "Passwords do not match."}) 
        return attrs 

    def create(self, validated_data): 
        validated_data.pop('password2') 
        user = User.objects.create_user(**validated_data) 
        return user 
    
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']  # Add any other fields you need
        
        
class LogoutSerializer(serializers.Serializer):
    refresh = CharField()