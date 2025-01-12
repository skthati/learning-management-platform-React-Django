from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions
from userauths.models import ( User, Profile )


# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = (permissions.AllowAny,)