# learning-management-platform-React-Django
Online training and Certification Platform using Python, Django, Mysql, React. 

## Django setup

1) Create two folders named `backend` and `frontend`.
2) cd to folder backend 
3) Create virtual environment using the command `python3 -m venv venv`
4) Activate the virtual environment using command `source venv/bin/activate`
5) Install Django using the command `python3 -m pip install Django`
6) To check what apps are installed use command `pip freeze`
7) Create Django project `django-admin startproject backend` // "backend ." will remove aditional folder.
8) Install required packages. Create new txt file and name it requirements.txt and run `pip install -r requirements.txt`
9) Install app core using command `python3 manage.py startapp core`.
10) Install app userauths using command `python3 manage.py startapp userauths`
11) Install app api using command `python3 manage.py startapp api`
12) Create file called .gitignore and add files which you want to ignore.
13) Add custom apps to `settings.py` 
    ```Python
    # Application definition

    INSTALLED_APPS = [
        'jazzmin',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        
        # Third party apps
        'core',
        'userauths',
        'api',
    ]

    ```Python
14) Run the server using command `python3 manage.py runserver`
15) Apply all migrations using command `python3 manage.py migrate`
16) Create superuser for admin using command `python3 manage.py createsuperuser`
17) Install jazzmin which will enhance features of admin panal.
    ![alt text](backend/backend/media/my_pics/jazzmin.png)


## Customize Jazzmin UI
18) Add below code in settings.py

    refere to below doc for further customization.
    `[Jazzmin documentation](https://django-jazzmin.readthedocs.io/configuration/)`
    ```Python
    JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Sandeep Learning Admin",
    "site_header": "Sandeep Learning Admin",
    "site_brand": "Sandeep Learning Admin",
    "welcome_sign": "Welcome to the Sandeep Learning Admin",
    "copyright": "Sloka IT Services Ltd",
    "show_ui_builder": True,

    }
    ```
## Static files
19) Go to `settings.py` and write below code.
    ```Python
    from pathlib import Path
    import os

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "templates")],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]


    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'templates')
    media_url = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    ```

## Import URLs
20) Go to `urls.py` and add below code

    ```Python
    from django.conf import settings
    from django.conf.urls.static import static
    ```
21) Also in urls.py add url path to static files
    ```Python
    urlpatterns = [
        path('admin/', admin.site.urls),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ```
## Creating custom users and models.
22) Go to userauths folder and open file models.py to update below code
    ```Python
    from django.db import models
    from django.contrib.auth.models import AbstractUser

    # Create your models here.

    class User(AbstractUser):
        username = models.CharField(max_length=255, unique=True)
        email = models.EmailField(max_length=255, unique=True)
        full_name = models.CharField(max_length=255, blank=True, null=True)
        otp = models.CharField(max_length=6, unique=True)

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = ['username']

        def __str__(self):
            return self.email
        
        def save(self, *args, **kwargs):
            email_username, full_name = self.email.split('@')
            if self.full_name == "" or self.full_name == None:
                self.full_name = email_username
            if self.username == "" or self.username == None:
                self.username = email_username
            super(User, self).save(*args, **kwargs)


    class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        image = models.FileField(upload_to='profile_pics/', default = "default-profile.png", blank=True, null=True)
        bio = models.TextField(blank=True, null=True)
        full_name = models.CharField(max_length=255, blank=True, null=True)
        country = models.CharField(max_length=255, blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            if self.full_name:
                return str(self.full_name)
            else:
                return str(self.user.full_name)

        def save(self, *args, **kwargs):
            if self.profile_pic == "":
                self.profile_pic = "profile_pics/default.png"
            if self.full_name == "" or self.full_name == None:
                self.full_name = self.user.username
            super(Profile, self).save(*args, **kwargs)


    ```
23) In userauths folder open admin.py file to update below code
    ```Python
    from django.contrib import admin
    from .models import User, Profile

    # Register your models here.

    class ProfileAdmin(admin.ModelAdmin):
        list_display = ['user', 'full_name', 'country', 'created_at', 'updated_at']
        search_fields = ['user__email', 'user__username', 'full_name', 'country']
        list_filter = ['created_at', 'updated_at']


    admin.site.register(User)
    admin.site.register(Profile, ProfileAdmin)
    ```
24) Output so far.
    ![admin-profile](backend/backend/static/admin-profile.gif)

25) Automatically create Profile when User is created.
    To do that go to folder userauths and open file models.py to write below code.
    ```Python
    from django.db.models.signals import post_save

    # End of models.py write below code.

    def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)   

    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    post_save.connect(create_profile, sender=User)
    post_save.connect(save_profile, sender=User)
    ```

26) ## Testing.
    Create a new user and confirm profile is created automatically. Also delete user and confirm profile is deleted.
    ![create-delete-user](backend/backend/static/delete-profile.gif)

27) ## Serialization
    Create a new file under api folder and name it serializer.py and copy below code

    ```Python
    from rest_framework import serializers
    from userauths.models import User, Profile

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = '__all__'

    class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = '__all__'

    ```

28) Install/Register 3rd party apps in settings.py
    Install rest_framework and corsheaders
    ```python
    # Application definition

    INSTALLED_APPS = [
        'rest_framework',
        'rest_framework_simplejwt.token_blacklist',
        'corsheaders',

    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
    ]

    ```

29) ## JWT Settings
    Code below is static and one off code written in settings.py
    ```Python
        SIMPLE_JWT = {
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True,
        'UPDATE_LAST_LOGIN': False,
        'ALGORITHM': 'HS256',
        'verifing_key': None,
        'AUDIENCE': None,
        'ISSUER': None,
        'jwk_url': None,
        'LEEWAY': 0,
        'AUTH_HEADER_TYPES': ('Bearer',),
        'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
        'USER_ID_FIELD': 'id',
        'USER_ID_CLAIM': 'user_id',
        'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
        'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
        'TOKEN_TYPE_CLAIM': 'token_type',
        'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
        'JTI_CLAIM': 'jti',
        'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
        'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
        'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    }
    ```
30) Cornheaders in settings.py
    ```Python
    CORS_ALLOW_ALL_ORIGINS = True

    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",

    ]
    ```

31) ## Token Serialization
    add below code to serializer.py file.
    ```Python
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


    class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
        @classmethod
        def get_token(cls, user):
            token = super(MyTokenObtainPairSerializer, cls).get_token(user)
            token['email'] = user.email
            token['username'] = user.username
            if hasattr(user, 'profile'):
                token['full_name'] = user.profile.full_name
            return token
    ```

32) Serializer class in api views
    Open views.py in API folder and write below code
    ```Python
    from django.shortcuts import render
    from api import serializer as api_serializer
    from rest_framework_simplejwt.views import TokenObtainPairView

    class MyTokenObtainPairView(TokenObtainPairView):
        serializer_class = api_serializer.MyTokenObtainPairSerializer
    ```
33) Add urls in api
    Create a new file urls.py in API folder and write below code.
    ```Python
    from api import views as api_views
    from django.urls import path

    urlpatterns = [
        path("user/token/", api_views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    ]
    ```
34) Add urls in backend folder
    Open file urls.py in backend folder and write below code.
    ```Python
    from django.urls import path, include

    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    ```
35) Token Output
    If we go to URL http://127.0.0.1:8000/api/user/token/ we can see the token and refresh token.
    ![Token Output](backend/backend/static/token.png)

36) Register User
    Open serializer.py in api folder and write below code
    ```Python
    from django.contrib.auth.password_validation import validate_password

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

            user = User.objects.create_user(
                email=validated_data['email'],
                username = email_username,
                full_name = full_name,
                password = validated_data['password1']
            )
            user.save()
            return user
    ```

37) Register User views
    Open views.py file in api folder and write below code.
    ```Python
    from rest_framework import generics, permissions
    from userauths.models import User, Profile

    class RegisterView(generics.CreateAPIView):
        queryset = User.objects.all()
        serializer_class = api_serializer.RegisterSerializer
        permission_classes = (permissions.AllowAny,)
    ```
38) Register urls 
    Open urls.py in api folder and write below code.
    ```Python
    from rest_framework_simplejwt.views import TokenObtainPairView

    urlpatterns = [
        path("user/token/", api_views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("user/register/", api_views.RegisterView.as_view(), name="register"),
        path("user/token/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),

    ]
    ```
39) Output for API Register
    ![Register User API](backend/backend/static/register.png)
40) Output for Token Refresh
    ![Token Refresh ](backend/backend/static/token-refresh.png)

41) ## Password reset email verify API
    Open models.py in backend folder and write below code
    ```Python

    refresh_token = models.CharField(max_length=1000, blank=True, null=True)
    ```
42) Open views.py in API folder and write below code.
    ```Python
    from rest_framework_simplejwt.tokens import RefreshToken
    class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializer.UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        email = self.kwargs.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            user.otp = generate_otp()
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)
            user.refresh_token = refresh_token
            uuidb64 = user.pk
            user.save()

            reset_link = f"http://l127.0.0.1:8000/reset-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"

            print(reset_link)
        
        return user
    ```
43) Register url 
    Open urls.py in api folder and write below code
    ```Python
    urlpatterns = [
        path("user/verify-email/<str:email>/", api_views.PasswordResetEmailVerifyAPIView.as_view(), name="verify_email"),
    ]
    ```

44) ## Reset Password
    Open views.py in api folder and write below code
    ```Python
    from rest_framework import generics, permissions, status

    class ResetPasswordAPIView(generics.CreateAPIView):
    serializer_class = api_serializer.UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload.get('otp')
        uuidb64 = payload.get('uuidb64')
        password = payload.get('password')
        refresh_token = payload.get('refresh_token')

        user = User.objects.filter(pk=uuidb64, otp = otp).first()
        if user:
            user.set_password(password)
            user.otp = None
            user.refresh_token = None
            user.save()
            return Response({'message': 'Password Reset Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
            
        
    ```

45) Register url 
    Open urls.py in api folder and write below code
    ```Python
    urlpatterns = [
        path("user/reset-password/", api_views.ResetPasswordAPIView.as_view(), name="reset_password"),
    ]
    ```

46) ## Environment variables
    Open settings.py and initialize variables.
    ```Python
    from environs import Env
    env = Env()
    BASE_DIR = Path(__file__).resolve().parent.parent
    env.read_env(os.path.join(BASE_DIR, '..', 'venv', '.env'))

    env.read_env()

    ```
47) Create a new file .env in folder venv and create your first variable.
    ```Python
    MAILGUN_SECREAT_KEY=yoursecreatkey
    ```
    In settings.py
    ```Python
    GMAIL_HOST="youremailaddress"
    GMAIL_PASSWORD="youremailpassword"
    ```
48) ## Email System
    Open settings.py and add below code
    ```Python
    # settings.py

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'  # For Gmail
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env("GMAIL_HOST")  # Replace with your email
    EMAIL_HOST_PASSWORD = env("GMAIL_PASSWORD") # Replace with your app-specific password


    ```
49) ### Email template folders
    create folder email inside backend/templates
    create file password_reset.html inside folder email
    write below code inside password_reset.html
    ```HTML
    <!DOCTYPE html>
    <html>
    <head>
        <title>Password Reset</title>
    </head>
    <body>
        <h1>Hello {{ username }},</h1>
        <p>We received a request to reset your password. You can reset it by clicking the link below:</p>
        <p><a href="{{ reset_link }}">Reset Password</a></p>
        <p>If you didn’t request a password reset, you can ignore this email.</p>
        <p>Thanks,<br>The Team</p>
    </body>
    </html>

    ```

50) Open views.py from api folder and write below code
    ```Python
    def send_simple_email(user, reset_link):
        subject = f"Hello {user.username}! Reset your password"
        from_email = settings.EMAIL_HOST_USER  # Must match EMAIL_HOST_USER
        recipient_list = [user.email]

        params = {
            'user': user,
            'reset_link': reset_link
        }

        text_body = render_to_string("email/password_reset.html", params)
        
        send_mail(subject, "", from_email, recipient_list, html_message=text_body)


    ```
51) Generate reset link and send to function send_simple_email
    ```Python
    class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
        serializer_class = api_serializer.UserSerializer
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

            reset_link = f"http://127.0.0.1:8000/reset-password/?otp={user.otp}&uuidb64={uuidb64}&refresh_token={refresh_token}"
            send_simple_email(user, reset_link)
            print(reset_link)
            
            return user
    ```

52) ### Output
    ![password reset request](backend/backend/static/password-reset-request.png)
    ![Email from app](backend/backend/static/email-from-app.png)

53) ## drf_yasg 
    ```Python
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Sandeep Learning Backend API",
            default_version='v1',
            description="API for Sandeep Learning",
            terms_of_service="http://wwww.sloka.co.nz",
            contact=openapi.Contact(email="support@sloka.co.nz"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns = [
        path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path("", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    ]

    ```
54) Register app 'drf_yasg' in settings.py

55) OUTPUT Swagger
    ![Swagger](backend/backend/static/swagger.gif)