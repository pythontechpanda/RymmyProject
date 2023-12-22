from django.shortcuts import render
from rest_framework import generics,status,views,permissions
from .models import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
import string
import random

# Create your views here.


# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#     def post(self,request):
#         user=request.data
#         print(">>>>>",user)
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         return Response(user_data, status=status.HTTP_201_CREATED)
    
    
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user_data = request.data.copy()

        # Generate username based on mobile number and a random string
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        random_string_var =str(random_string)
        
        username = f"{user_data['mobile_no'][:4]}{random_string_var}"
        user_data['username'] = username

        # Set the password the same as the username
        user_data['password'] = username

        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


