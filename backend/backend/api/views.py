from django.shortcuts import render
from api import serializer as api_serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status
from userauths.models import ( User, Profile )
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import decimal
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

class InstructorView(ModelViewSet):
    queryset = api_models.Instructor.objects.all()
    serializer_class = api_serializer.InstructorSerializer
    permission_classes = (permissions.AllowAny,)

    # def get_queryset(self):
    #     return self.queryset.all()

class CategoryView(ModelViewSet):
    queryset = api_models.Category.objects.filter(active = True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = (permissions.AllowAny,)

class MyCategoryView(ModelViewSet):
    queryset = api_models.Category.objects.filter(active = True)
    serializer_class = api_serializer.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'  # Use 'slug' instead of the default 'pk'

    def get_queryset(self):
        # Get the slug from url params
        slug = self.kwargs.get('slug', None)
        if slug:
            queryset = api_models.Category.objects.filter(slug=slug, active=True)
        else:
            queryset = api_models.Category.objects.filter(active=True)
        return queryset

class CourseView(ModelViewSet):
    queryset = api_models.Course.objects.filter(active = True) # platform_status = "Published", 
    serializer_class = api_serializer.CourseSerializer
    permission_classes = (permissions.AllowAny,)

class MyCourseView(ModelViewSet):
    queryset = api_models.Course.objects.filter(active = True) # platform_status = "Published", 
    serializer_class = api_serializer.CourseSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'slug'  # Use 'slug' instead of the default 'pk'

    def get_queryset(self):
        # Get the slug from url params
        print(self.kwargs)
        slug = self.kwargs.get('slug', None)
        id = self.kwargs.get('id', None)
        if slug:
            queryset = api_models.Course.objects.filter(slug=slug, active=True)
        else:
            queryset = api_models.Course.objects.filter(active=True)
        return queryset
    
class ChapterView(ModelViewSet):
    queryset = api_models.Chapter.objects.all()
    serializer_class = api_serializer.ChapterSerializer
    permission_classes = (permissions.AllowAny,)

class ChapterListView(ModelViewSet):
    queryset = api_models.ChapterList.objects.all()
    serializer_class = api_serializer.ChapterListSerializer
    permission_classes = (permissions.AllowAny,)

class Question_AnswerView(ModelViewSet):
    queryset = api_models.Question_Answer.objects.all()
    serializer_class = api_serializer.Question_AnswerSerializer
    permission_classes = (permissions.AllowAny,)

class Question_Answer_MessageView(ModelViewSet):
    queryset = api_models.Question_Answer_Message.objects.all()
    serializer_class = api_serializer.Question_Answer_MessageSerializer
    permission_classes = (permissions.AllowAny,)

class CartView(ModelViewSet):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = (permissions.AllowAny,)

class MyCartView(ModelViewSet):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        payload = request.data
        user = request.user
        user_id = payload.get('user_id')
        course_id = payload.get('course')
        cart_id = payload.get('cart_id')
        price = payload.get('price')
        country = payload.get('country')
        
        course = api_models.Course.objects.filter(id=course_id).first()
        print(f"{course} + {course_id}")

        if user:
            user = User.objects.filter(id=user_id).first()
        else:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            country_object = api_models.Country.objects.filter(country_name=country).first()
            if country_object:
                country = country_object.country_name
        except:
            country = "New Zealand"
        
        if country_object:
            tax = country_object.tax/100
        else:
            tax = 0
        
        if not course:
            return Response({'message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart = api_models.Cart.objects.filter(cart_id = cart_id, course=course).first()
        
        if cart:
            cart.cart_id = cart_id
            cart.course = course
            cart.user = user
            cart.price = price
            cart.country = country
            cart.tax = decimal.Decimal(price) * decimal.Decimal(tax)
            cart.total = decimal.Decimal(price) + decimal.Decimal(cart.tax) 
            cart.save()
            return Response({'message': 'Course added to cart'}, status=status.HTTP_200_OK)
        else:
            # Create a new cart
            cart = api_models.Cart()

            cart.cart_id = cart_id
            cart.course = course
            cart.user = user
            cart.price = price
            cart.country = country
            cart.tax = decimal.Decimal(price) * decimal.Decimal(tax)
            cart.total = decimal.Decimal(price) + decimal.Decimal(cart.tax)
            cart.save()
            return Response({'message': 'Cart created successfully'}, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
class CartOrderView(ModelViewSet):
    queryset = api_models.CartOrder.objects.all()
    serializer_class = api_serializer.CartOrderSerializer
    permission_classes = (permissions.AllowAny,)
    # lookup_field = 'cart_id'  # Use 'cart_id' instead of the default 'pk'

    # def get_queryset(self):
    #     cart_id = self.kwargs.get('cart_id', None)
    #     print(cart_id)
    #     if cart_id:
    #         queryset = api_models.CartOrder.objects.filter(cart_id=cart_id)
    #     else:
    #         queryset = api_models.CartOrder.objects.all()
    #     return queryset

class CartOrderListView(ModelViewSet):
    queryset = api_models.CartOrderList.objects.all()
    serializer_class = api_serializer.CartOrderListSerializer
    permission_classes = (permissions.AllowAny,)

class MyCartOrderListView(ModelViewSet):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        cart_id = self.kwargs.get('cart_id', None)
        print(cart_id)
        if cart_id:
            queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        else:
            queryset = api_models.Cart.objects.all()
        return queryset
    
    def destroy(self, request, *args, **kwargs):
        cart_id = self.kwargs.get('cart_id', None)
        item_id = self.kwargs.get('pk', None)

        if not cart_id or not item_id:
            return Response(
                {
                    "error": "Cart ID or List ID does not match."
                }, status=status.HTTP_400_BAD_REQUEST,
            )
        
        cart_item = api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first()
        if cart_item:
            cart_item.delete()
            return Response(
                {
                    "error": "Cart Item deleted Successfully."
                }, status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {
                    "error": "Cart item not found."
                }, status=status.HTTP_404_NOT_FOUND
            )

    
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
        # return super().retrieve(request, *args, **kwargs)

class MyCartStatsView(ModelViewSet):
    # queryset = api_models.Cart.objects.all()
    serializer_class = api_serializer.CartSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'cart_id'  # Use 'cart_id' instead of the default 'pk'

    def get_queryset(self):
        cart_id = self.kwargs.get('cart_id', None)
        if cart_id:
            queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        else:
            queryset = api_models.Cart.objects.all()
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.0
        total_tax = 0.0
        grand_total = 0.0

        for item in queryset:
            total_price += float(item.price)
            total_tax += float(item.tax)
            grand_total += round(float(item.total), 2)
        
        data = {
            "price": total_price,
            "tax": total_tax,
            "grand_total": grand_total
        }

        return Response(data)



class CertificateView(ModelViewSet):
    queryset = api_models.Certificate.objects.all()
    serializer_class = api_serializer.CertificateSerializer
    permission_classes = (permissions.AllowAny,)

class CompletedLessonView(ModelViewSet):
    queryset = api_models.CompletedLesson.objects.all()
    serializer_class = api_serializer.CompletedLessonSerializer
    permission_classes = (permissions.AllowAny,)

class EnrolledCourseView(ModelViewSet):
    queryset = api_models.EnrolledCourse.objects.all()
    serializer_class = api_serializer.EnrolledCourseSerializer
    permission_classes = (permissions.AllowAny,)

class NotesView(ModelViewSet):
    queryset = api_models.Notes.objects.all()
    serializer_class = api_serializer.NotesSerializer
    permission_classes = (permissions.AllowAny,)

class ReviewsView(ModelViewSet):
    queryset = api_models.Reviews.objects.all()
    serializer_class = api_serializer.ReviewsSerializer
    permission_classes = (permissions.AllowAny,)

class NotificationsView(ModelViewSet):
    queryset = api_models.Notifications.objects.all()
    serializer_class = api_serializer.NotificationsSerializer
    permission_classes = (permissions.AllowAny,)

class CouponView(ModelViewSet):
    queryset = api_models.Coupon.objects.all()
    serializer_class = api_serializer.CouponSerializer
    permission_classes = (permissions.AllowAny,)

class WishlistView(ModelViewSet):
    queryset = api_models.Wishlist.objects.all()
    serializer_class = api_serializer.WishlistSerializer
    permission_classes = (permissions.AllowAny,)

class CountryView(ModelViewSet):
    queryset = api_models.Country.objects.all()
    serializer_class = api_serializer.CountrySerializer
    permission_classes = (permissions.AllowAny,)
