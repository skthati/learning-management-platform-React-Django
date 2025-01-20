from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status
from userauths.models import ( User, Profile )
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from api import models as api_models


# Create your views here.


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializer.RegisterSerializer
    permission_classes = (permissions.AllowAny,)


def generate_otp(Len = 6):
    import random
    return "".join([str(random.randint(0, 9)) for _ in range(Len)])



def send_simple_email(user, reset_link):
    subject = f"Hello {user.username}! Reset your password"
    from_email = settings.EMAIL_HOST_USER  # Must match EMAIL_HOST_USER
    recipient_list = [user.email]

    params = {
        'user': user.username,
        'reset_link': reset_link
    }

    text_body = render_to_string("email/password_reset.html", params)
    
    send_mail(subject, "", from_email, recipient_list, html_message=text_body)


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.UserWithoutPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        email = self.kwargs.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            raise Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
    
        user.otp = generate_otp()
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh.access_token)
        user.refresh_token = refresh_token
        # uuidb64 = user.pk
        uuidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        user.save()

        reset_link = f"http://localhost:5173/reset-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"
        send_simple_email(user, reset_link)
        print(reset_link)

        return user, reset_link
    
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        if isinstance(user, Response):
            return user
        user, reset_link = user
        serializer = self.get_serializer(user)
        return Response({
            'message': 'Email sent successfully',
            'data': serializer.data,
            'reset_link': reset_link,
        }, status=status.HTTP_200_OK)


class ResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload.get('otp')
        uuidb64 = payload.get('uuidb64')
        password = payload.get('password')
        refresh_token = payload.get('refresh_token')
        print(otp, uuidb64, password, refresh_token)

        try:
            user_id = int(urlsafe_base64_decode(uuidb64))
            user = User.objects.filter(pk=user_id, otp=otp).first()
        except (ValueError, TypeError):
            user = None

        if user and user.refresh_token == refresh_token:
            user.set_password(password)
            user.otp = None
            user.refresh_token = None
            user.save()
            return Response({'message': 'Password Reset Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)


class InstructorView(generics.ListCreateAPIView):
    queryset = api_models.Instructor.objects.all()
    serializer_class = api_serializer.InstructorSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return self.queryset.all()


class CategoryView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active = True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = (permissions.AllowAny,)

