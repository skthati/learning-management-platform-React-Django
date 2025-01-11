from django.contrib import admin
from .models import User, Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'country', 'created_at', 'updated_at']
    search_fields = ['user__email', 'user__username', 'full_name', 'country']
    list_filter = ['created_at', 'updated_at']


admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)