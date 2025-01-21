from api import views as api_views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'instructors', api_views.InstructorView)
router.register(r'categories', api_views.CategoryView)
router.register(r'courses', api_views.CourseView)

urlpatterns = [
    path("user/token/", api_views.MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("user/register/", api_views.RegisterView.as_view(), name="register"),
    path("user/token/refresh/", TokenObtainPairView.as_view(), name="token_refresh"),
    path("user/verify-email/<str:email>/", api_views.PasswordResetEmailVerifyAPIView.as_view(), name="verify_email"),
    path("user/reset-password/", api_views.ResetPasswordAPIView.as_view(), name="reset_password"),
    path("", include(router.urls)),

    # Core Routes
    # path("instructor/", api_views.InstructorView.as_view(), name="instructor_view"),
    # path("category/", api_views.CategoryView.as_view(), name="category"),
    # path("course/", api_views.CourseView.as_view(), name="course")
]

