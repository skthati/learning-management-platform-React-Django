from rest_framework import serializers
from userauths.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        if hasattr(user, 'profile'):
            token['full_name'] = user.profile.full_name
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password1', 'password2']

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs
    
    def create(self, validated_data):
        email_username, _ = validated_data['email'].split('@')
        
        full_name = validated_data.get('full_name', email_username)
        print(full_name, email_username)

        user = User.objects.create_user(
            email=validated_data['email'],
            username = email_username,
            full_name = full_name,
            password = validated_data['password1']
        )


        user.save()

        return user
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

