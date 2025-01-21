from django.db import models
from userauths.models import User, Profile
from django.utils.text import slugify
import random
from shortuuid.django_fields import ShortUUIDField



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

    # def Students(self):
    #     return CartOrderItem.objects.filter(course__instructor=self)
    
    def Courses(self):
        return Course.objects.filter(instructor=self)
    
    def ReviewsCount(self):
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
    
    def CourseCount(self):
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







