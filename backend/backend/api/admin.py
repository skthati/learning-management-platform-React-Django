from django.contrib import admin
# from .models import Instructor, Category, Course
# from api.models import models
from .models import (
    Instructor, 
    Category, 
    Course , 
    Chapter, 
    ChapterList, 
    Question_Answer,
    Question_Answer_Message,
    Cart,
    CartOrder,
    CartOrderList,
    Certificate,
    CompletedLesson,
    EnrolledCourse,
    Notes,
    Reviews,
    Notifications,
    Coupon,
    Wishlist,
    Country,
)

class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'country', 'created_at', 'updated_at']
    search_fields = ['user__username', 'full_name', 'country']
    list_filter = ['country', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Show the newest instructors first


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    search_fields = ['title']
    list_filter = ['created_at', 'updated_at']
    ordering = ['title']  # Sort categories alphabetically


class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'instructor', 'price', 'created_at', 'updated_at']
    search_fields = ['title', 'category__title', 'instructor__full_name']
    list_filter = ['category', 'price', 'created_at', 'updated_at']
    ordering = ['-created_at']  # Show the newest courses first
    list_editable = ['price']  # Allow quick editing of the price from the admin list view


# Register your models with the admin
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Chapter, )
admin.site.register(ChapterList, )
admin.site.register(Question_Answer, )
admin.site.register(Question_Answer_Message, )
admin.site.register(Cart, )
admin.site.register(CartOrder, )
admin.site.register(CartOrderList, )
admin.site.register(Certificate, )
admin.site.register(CompletedLesson, )
admin.site.register(EnrolledCourse, )
admin.site.register(Notes, )
admin.site.register(Reviews, )
admin.site.register(Notifications, )
admin.site.register(Coupon, )
admin.site.register(Wishlist, )
admin.site.register(Country, )