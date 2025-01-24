from rest_framework import serializers
from userauths.models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from api import models as api_models


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

class UserWithoutPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ChapterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.ChapterList
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    chapter_lists = ChapterListSerializer(many=True)
    class Meta:
        model = api_models.Chapter
        fields = [
            "course",
            "title",
            "description",
            "chapter_id",
            "created_at",
            "updated_at",
            "chapter_lists",
        ]

class Question_Answer_MessageSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = api_models.Question_Answer_Message
        fields = [
            "course",
            "question",
            "user",
            "qam_id",
            "title",
            "message",
            "created_at",
            "updated_at",
            "profile",
        ]

class Question_AnswerSerializer(serializers.ModelSerializer):
    messages = Question_Answer_MessageSerializer(many=True)
    profile = ProfileSerializer(many=False)
    class Meta:
        model = api_models.Question_Answer
        fields = [
            "course",
            "user",
            "q_id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "messages",
            "profile",
        ]

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Cart
        fields = '__all__'

class CartOrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.CartOrderList
        fields = '__all__'

class CartOrderSerializer(serializers.ModelSerializer):
    order_list = CartOrderListSerializer(many=True)
    class Meta:
        model = api_models.CartOrder
        fields = [
            "student",
            "instructor",
            "sub_total",
            "tax",
            "discount_total",
            "total",
            "grand_total",
            "payment_status",
            "full_name",
            "email",
            "country",
            "coupon",
            "stripe_session_id",
            "order_id",
            "created_at",
            "updated_at",
            "order_list",
        ]

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Certificate
        fields = '__all__'

class CompletedLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.CompletedLesson
        fields = '__all__'

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Notes
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)
    class Meta:
        model = api_models.Reviews
        fields = [
            "course",
            "user",
            "review",
            "rating",
            "reply",
            "active",
            "created_at",
            "updated_at",
            "profile",
        ]

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Notifications
        fields = '__all__'

class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Coupon
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Wishlist
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Country
        fields = '__all__'

class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = ChapterListSerializer(many=True)
    completed_lesson = CompletedLessonSerializer(many=True)
    curriculum = ChapterSerializer(many=True)
    notes = NotesSerializer(many=True)
    question_answer = Question_AnswerSerializer(many=True)
    review = ReviewsSerializer(many=True)
    class Meta:
        model = api_models.EnrolledCourse
        fields = [
            "course",
            "user",
            "instructor",
            "enrollment_id",
            "order_list",
            "created_at",
            "updated_at",
            "lectures",
            "completed_lesson",
            "curriculum",
            "notes",
            "question_answer",
            "review",
        ]

class CourseSerializer(serializers.ModelSerializer):
    students = EnrolledCourseSerializer(many=True, required=False, read_only=True)
    curriculum = ChapterSerializer(many=True, required=False, read_only=True)
    lectures = ChapterListSerializer(many=True, required=False, read_only=True)
    # average_rating = ReviewsSerializer(many=True, required=False, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    # reviews_count = str(ReviewsSerializer(many=False, required=False, read_only=True))
    reviews_count = serializers.IntegerField(read_only=True)
    reviews = ReviewsSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = api_models.Course
        fields = [
            "category",
            "instructor",
            "course_id",
            "file",
            "image",
            "active",
            "title",
            "slug",
            "description",
            "price",
            "language",
            "level",
            "instructor_status",
            "platform_status",
            "featured",
            "created_at",
            "updated_at",
            "students",
            "curriculum",
            "lectures",
            "average_rating",
            "reviews_count",
            "reviews",
        ]

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = api_models.Course
#         fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    course_count = str(CourseSerializer(many=True))
    slug = serializers.CharField(allow_null=True, required=False)
    class Meta:
        model = api_models.Category
        fields = [
            "title",
            "image",
            "active",
            "slug",
            "created_at",
            "updated_at",
            "course_count",
        ]

class InstructorSerializer(serializers.ModelSerializer):
    students = CartOrderListSerializer(many=True)
    # courses = CourseSerializer(many=True)
    # reviews_count = CourseSerializer(many=True)
    class Meta:
        model = api_models.Instructor
        fields = [
            "user",
            "image",
            "full_name",
            "bio",
            "country",
            "facebook",
            "twitter",
            "linkedin",
            "created_at",
            "updated_at",
            "students",
            # "courses",
            "reviews_count",
        ]
