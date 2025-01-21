from django.contrib import admin
from .models import Instructor, Category, Course


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

