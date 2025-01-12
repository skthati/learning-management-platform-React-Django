from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("user/token/", api_views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/register/", api_views.RegisterView.as_view(), name="register"),
    path("user/token/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),

]

