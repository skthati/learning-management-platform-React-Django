from api import views as api_views
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'instructors', api_views.InstructorView)
router.register(r'categories', api_views.CategoryView)
router.register(r'courses', api_views.CourseView)
router.register(r'chapters', api_views.ChapterView)
router.register(r'chapter-lists', api_views.ChapterListView)
router.register(r'question-answers', api_views.Question_AnswerView)
router.register(r'question-answer-messages', api_views.Question_Answer_MessageView)
router.register(r'cart', api_views.CartView)
router.register(r'cart-orders', api_views.CartOrderView)
router.register(r'cart-order-lists', api_views.CartOrderListView)
router.register(r'certificates', api_views.CertificateView)
router.register(r'completed-lessons', api_views.CompletedLessonView)
router.register(r'enrolled-courses', api_views.EnrolledCourseView)
router.register(r'notes', api_views.NotesView)
router.register(r'reviews', api_views.ReviewsView)
router.register(r'notifications', api_views.NotificationsView)
router.register(r'coupons', api_views.CouponView)
router.register(r'wishlists', api_views.WishlistView)
router.register(r'countries', api_views.CountryView)


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
    path('categories/<slug:slug>/', api_views.CategoryView.as_view({'get':'list'}), name='category-by-slug'),
    path('courses/<slug:slug>/', api_views.CourseView.as_view({'get':'list'}), name='course-by-slug'),

]

