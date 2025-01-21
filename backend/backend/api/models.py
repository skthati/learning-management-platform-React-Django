from django.db import models
from userauths.models import User, Profile
from django.utils.text import slugify
import random
import math
from shortuuid.django_fields import ShortUUIDField
from moviepy import VideoFileClip



LANGUAGE = (
    ("English", "English"),
    ("Hindi", "Hindi"),
    ("Telugu", "Telugu"),
)

LEVEL = (
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advanced", "Advanced"),
)

INSTRUCTOR_STATUS = (
    ("Draft", "Draft"),
    ("Published", "Published"),
    ("Disabled", "Disabled"),
)

PLATFORM_STATUS = (
    ("Review", "Review"),
    ("Rejected", "Rejected"),
    ("Approved", "Approved"),
)

PAYMENT_STATUS = (
    ("Processing", "Processing"),
    ("Paid", "Paid"),
    ("Unpaid", "Unpaid"),
)

RATING = (
    (1, "⭐" ),
    (2, "⭐⭐" ),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐"),
)

NOTIFICATION_TYPE = (
    ("EMAIL", "EMAIL"),
    ("TEXT", "TEXT"),
)

# Create your models here.
class Instructor(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    image = models.FileField(upload_to='instructor_pics/', default = "default-profile.png", blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def Students(self):
        return CartOrder.objects.filter(course__instructor=self)
    
    def courses(self):
        return Course.objects.filter(instructor=self)
    
    def reviews_count(self):
        return Course.objects.filter(course__instructor=self).count()

class Category(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField(upload_to='category_pics/', default = "default-category.png", blank=True, null=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ['title']

    def __str__(self):
        return self.title
    
    def course_count(self):
        return Course.objects.filter(category = self).count()
    
    def save(self, *args, **kwargs ):
        if (self.slug == "" or self.slug == None):
            self.slug = slugify(self.title)
        return super(Category, self).save(*args, **kwargs)
    

class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    course_id = models.CharField(unique=True, max_length=9, editable=False)
    file = models.FileField(upload_to="course_files/", null=True, blank=True)
    image = models.FileField(upload_to="course_files/", null=True, blank=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(LANGUAGE, max_length=20, default="English")
    level = models.CharField(LEVEL, default="Beginner", max_length=20,)
    instructor_status = models.CharField(INSTRUCTOR_STATUS, default="Draft", max_length=20,)
    platform_status = models.CharField(PLATFORM_STATUS, default="Review", max_length=20,)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.course_id:
            while True:
                # Generate a random 6-digit number
                numeric_part = f"{random.randint(100000, 999999)}"
                course_id = f"CO-{numeric_part}"
                # Check if the generated course_id is unique
                if not Course.objects.filter(course_id=course_id).exists():
                    self.course_id = course_id
                    break

        if not self.slug:
            self.slug = slugify(self.title)

        super(Course, self).save(*args, **kwargs)
    
    def students(self):
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return ChapterList.objects.filter(chapter__course=self)
    
    def lectures(self):
        return ChapterList.objects.filter(chapter__course=self)
    
    def average_rating(self):
        average_rating = Reviews.objects.filter(course=self).aggregate(avg_rating=models.Avg('rating'))
        return average_rating['avg_rating']
    
    def reviews_count(self):
        return Reviews.objects.filter(course=self, active=True).count()
    
    def reviews(self):
        return Reviews.objects.filter(course=self, active=True)
    

class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter_id = models.CharField(unique=True, max_length=9, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.chapter_id:
            while True:
                # Generate a random 6-digit number
                numeric_part = f"{random.randint(100000, 999999)}"
                chapter_id = f"CH-{numeric_part}"
                # Check if the generated chapter_id is unique
                if not Chapter.objects.filter(chapter_id=chapter_id).exists():
                    self.chapter_id = chapter_id
                    break

        super(Chapter, self).save(*args, **kwargs)
    
    def chapter_lists(self):
        return ChapterList.objects.filter(chapter=self)

class ChapterList(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="chapter_lists")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    chapter_list_id = models.CharField(unique=True, max_length=9, editable=False)
    file = models.FileField(upload_to='course_files/', null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.chapter.title}"
    
    def save(self, *args, **kwargs):
        if not self.chapter_list_id:
            while True:
                # Generate a random 6-digit number
                numeric_part = f"{random.randint(100000, 999999)}"
                chapter_list_id = f"CL-{numeric_part}"
                # Check if the generated chapter_list_id is unique
                if not ChapterList.objects.filter(chapter_list_id=chapter_list_id).exists():
                    self.chapter_list_id = chapter_list_id
                    break
        
        if self.file:
            clip = VideoFileClip(self.file.path)
            duration_seconds = clip.duration
            minutes, seconds = divmod(duration_seconds, 60)
            minutes = math.floor(minutes)
            seconds = math.floor(seconds)
            self.content_duration = f"{minutes}:{seconds}"
            
        super(ChapterList, self).save(*args, **kwargs)


class Question_Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    q_id = models.CharField(unique=True, max_length=10, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']
    
    def messages(self):
        return Question_Answer_Message.objects.filter(question=self)
    
    def profile(self):
        return Profile.objects.get(user=self.user)

    def save(self, *args, **kwargs):
        if not self.q_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                q_id = f"QA-{numeric_part}"
                # Check if the generated q_id is unique
                if not Question_Answer.objects.filter(q_id=q_id).exists():
                    self.q_id = q_id
                    break

        super(Question_Answer, self).save(*args, **kwargs)

class Question_Answer_Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    qam_id = models.CharField(unique=True, max_length=10, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.user.username}"
    
    class Meta:
        ordering = ['created_at']
    
    def profile(self):
        return Profile.objects.get(user=self.user)
    
    def save(self, *args, **kwargs):
        if not self.qam_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                qam_id = f"QAM-{numeric_part}"
                # Check if the generated qam_id is unique
                if not Question_Answer_Message.objects.filter(qam_id=qam_id).exists():
                    self.qam_id = qam_id
                    break

        super(Question_Answer_Message, self).save(*args, **kwargs)


class Cart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    cart_id = models.CharField(unique=True, max_length=11, editable=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    country = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title} - {self.cart_id}"
    
    def save(self, *args, **kwargs):
        if not self.cart_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                cart_id = f"CART-{numeric_part}"
                # Check if the generated cart_id is unique
                if not Cart.objects.filter(cart_id=cart_id).exists():
                    self.cart_id = cart_id
                    break

        super(Cart, self).save(*args, **kwargs)

class CartOrder(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ManyToManyField(Instructor, blank=True)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(choices=PAYMENT_STATUS, default="Processing", max_length=20,)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    coupon = models.ManyToManyField("api.Coupon", blank=True)
    stripe_session_id = models.CharField(max_length=1000, null=True, blank=True)
    order_id = models.CharField(unique=True, max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order ID: {self.order_id}"
    
    class Meta:
        ordering = ['created_at']
    
    def order_list(self):
        return CartOrderList.objects.filter(order=self)

    def save(self, *args, **kwargs):
        if not self.order_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                order_id = f"ORD-{numeric_part}"
                # Check if the generated order_id is unique
                if not CartOrder.objects.filter(order_id=order_id).exists():
                    self.order_id = order_id
                    break

        super(CartOrder, self).save(*args, **kwargs)
    
class CartOrderList(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name="cart_order_list")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="order_item")
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, null=True, blank=True)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    discount_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    coupon = models.ForeignKey("api.Coupon",on_delete=models.SET_NULL, null=True, blank=True)
    coupon_applied = models.BooleanField(default=False)
    ord_id = models.CharField(unique=True, max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order ID: {self.ord_id}"
    
    class Meta:
        ordering = ['created_at']
    
    def order_id(self):
        return f"Order ID: {self.order.order_id}"
    
    def payment_status(self):
        return f"Payment Status: {self.order.payment_status}"

    def save(self, *args, **kwargs):
        if not self.ord_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                ord_id = f"COR-{numeric_part}"
                # Check if the generated ord_id is unique
                if not CartOrderList.objects.filter(ord_id=ord_id).exists():
                    self.ord_id = ord_id
                    break

        super(CartOrderList, self).save(*args, **kwargs)

class Certificate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    certificate_id = models.CharField(unique=True, max_length=10, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.title}"

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                certificate_id = f"CER-{numeric_part}"
                # Check if the generated certificate_id is unique
                if not Certificate.objects.filter(certificate_id=certificate_id).exists():
                    self.certificate_id = certificate_id
                    break

        super(Certificate, self).save(*args, **kwargs)

class CompletedLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    chapter_list = models.ForeignKey(ChapterList, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.title}"

class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, )
    enrollment_id = models.CharField(unique=True, max_length=10, editable=False)
    order_list = models.ForeignKey(CartOrderList, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.title}"
    
    def lectures(self):
        return ChapterList.objects.filter(chapter__course=self.course)
    
    def completed_lesson(self):
        return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return Chapter.objects.filter(course=self.course)
    
    def notes(self):
        return Notes.objects.filter(course=self.course, user=self.user)
    
    def question_answer(self):
        return Question_Answer.objects.filter(course=self.course)
    
    def review(self):
        return Reviews.objects.filter(course=self.course, user=self.user).first()

    def save(self, *args, **kwargs):
        if not self.enrollment_id_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                enrollment_id_id = f"ORD-{numeric_part}"
                # Check if the generated enrollment_id_id is unique
                if not EnrolledCourse.objects.filter(enrollment_id_id=enrollment_id_id).exists():
                    self.enrollment_id_id = enrollment_id_id
                    break

        super(EnrolledCourse, self).save(*args, **kwargs)

class Notes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    note_id = models.CharField(unique=True, max_length=10, editable=False)
    title = models.CharField(max_length=255, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.note_id:
            while True:
                # Generate a random 7-digit number
                numeric_part = f"{random.randint(100000, 9999999)}"
                note_id = f"QA-{numeric_part}"
                # Check if the generated note_id is unique
                if not Notes.objects.filter(note_id=note_id).exists():
                    self.note_id = note_id
                    break

        super(Notes, self).save(*args, **kwargs)

    
class Reviews(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.TextField(null=True, blank=True)
    rating = models.CharField(choices=RATING, max_length=20,)
    reply = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.title
    
    def profile(self):
        return Profile.objects.get(user=self.user)


class Notifications(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_list = models.ForeignKey(CartOrderList, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Reviews, on_delete=models.SET_NULL, null=True, blank=True)
    notification_type = models.CharField(choices=NOTIFICATION_TYPE, max_length=50)
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_type

class Coupon(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=50)
    discount_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Wishlist(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course

class Country(models.Model):
    country_name = models.CharField(max_length=100, )
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.country_name